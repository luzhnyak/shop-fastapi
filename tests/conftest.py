from httpx import AsyncClient, ASGITransport
import asyncio
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from pydantic_settings import BaseSettings, SettingsConfigDict
from fnmatch import fnmatch

from app.db.db import Base, get_db
from app.main import app
from app.models.company import Company
from app.models.user import User
from app.models.membership import Membership, MembershipStatus
from app.models.quiz import Quiz, Question, AnswerOption, QuizResult


class PostgresSettings(BaseSettings):
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str
    TEST_POSTGRES_DB: str
    TEST_POSTGRES_PORT: int = 5432
    TEST_POSTGRES_HOST: str = "localhost"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.TEST_POSTGRES_USER}:{self.TEST_POSTGRES_PASSWORD}@"
            f"{self.TEST_POSTGRES_HOST}:{self.TEST_POSTGRES_PORT}/{self.TEST_POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


test_db_settings = PostgresSettings()

test_engine = create_async_engine(test_db_settings.DATABASE_URL, echo=True)

TestSessionLocal = async_sessionmaker(
    bind=test_engine, autoflush=False, expire_on_commit=False
)

users_data = [
    {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "password1",
    },
    {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
        "password": "password2",
    },
]

companies_data = [
    {"name": "John", "description": "Doe"},
    {"name": "Jane", "description": "Smith"},
]


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def db_session():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()

    async with TestSessionLocal() as session:
        for data in users_data:
            new_user = User(
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                hashed_password=data["password"],
            )
            session.add(new_user)

        for data in companies_data:
            new_companie = Company(
                name=data["name"], description=data["description"], owner_id=1
            )
            session.add(new_companie)

        await session.commit()
        yield session
        await session.close()


@pytest.fixture(scope="session")
def override_get_db(db_session):
    def _get_db():
        yield db_session

    return _get_db


@pytest.fixture(scope="session")
async def client(override_get_db):
    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


class FakeRedisService:
    def __init__(self):
        self.storage = {}

    async def setex(self, key, ttl, value):
        self.storage[key] = value
        return True

    async def get(self, key):
        return self.storage.get(key)

    async def keys(self, pattern="*"):
        return [key for key in self.storage if fnmatch(key, pattern)]


@pytest.fixture
def fake_redis_service():
    return FakeRedisService()
