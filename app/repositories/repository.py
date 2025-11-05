from sqlalchemy import insert, select, update, delete, RowMapping, func
from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC, abstractmethod

from app.db.error_handler import db_error_handler


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict) -> RowMapping:
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, **filter_by):
        raise NotImplementedError

    @abstractmethod
    async def find_many(self, skip: int, limit: int, **filter_by):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, **filter_by):
        raise NotImplementedError

    @abstractmethod
    async def edit_one(self, id: int, data: dict) -> RowMapping:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id: int) -> RowMapping:
        raise NotImplementedError

    @abstractmethod
    async def count_all(self, **filter_by) -> int:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    @db_error_handler
    async def add_one(self, data: dict) -> RowMapping:
        stmt = (
            insert(self.model).values(**data).returning(*self.model.__table__.columns)
        )
        res = await self.session.execute(stmt)
        result = res.fetchone()
        if result is None:
            raise ValueError("Failed to add record")
        return result._mapping

    @db_error_handler
    async def add_many(self, data_list: list[dict]) -> list[RowMapping]:
        if not data_list:
            return []
        stmt = (
            insert(self.model)
            .values(data_list)
            .returning(*self.model.__table__.columns)
        )
        res = await self.session.execute(stmt)
        return [row._mapping for row in res.fetchall()]

    @db_error_handler
    async def edit_one(self, id: int, data: dict) -> RowMapping:
        stmt = (
            update(self.model)
            .values(**data)
            .filter_by(id=id)
            .returning(*self.model.__table__.columns)
        )
        res = await self.session.execute(stmt)
        result = res.fetchone()
        if result is None:
            raise ValueError("Record not found")
        return result._mapping

    @db_error_handler
    async def find_one(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    @db_error_handler
    async def find_all(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    @db_error_handler
    async def find_many(self, skip: int, limit: int, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt.offset(skip).limit(limit))
        return res.scalars().all()

    @db_error_handler
    async def delete_one(self, id: int) -> RowMapping:
        stmt = (
            delete(self.model).filter_by(id=id).returning(*self.model.__table__.columns)
        )
        res = await self.session.execute(stmt)
        result = res.fetchone()
        if result is None:
            raise ValueError("Record not found")
        return result._mapping

    @db_error_handler
    async def delete_all(self, **filter_by) -> int:
        stmt = delete(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        result = res.rowcount
        if result is None:
            raise ValueError("No records found to delete")

        return result

    @db_error_handler
    async def count_all(self, **filter_by) -> int:
        stmt = select(func.count()).select_from(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        return res.scalar()
