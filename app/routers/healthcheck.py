from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db import get_db
from app.db.redis import RedisService


router = APIRouter(tags=["Test"])


@router.get("/healthcheck")
def healthcheck():
    return {"status_code": 200, "detail": "ok", "result": "working"}


@router.get("/test_postgres")
async def check_postgres(session: AsyncSession = Depends(get_db)):
    try:
        result = await session.execute(text("SELECT 1"))
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database is not configured correctly",
            )
        return {"message": "Postgres connection test successful"}
    except Exception as e:
        return {"message": f"Postgres connection test failed: {str(e)}"}


@router.get("/test_redis")
async def check_redis(redis_service: RedisService = Depends()):
    try:
        await redis_service.set("test_key", "test_value")
        value = await redis_service.get("test_key")
        assert value == "test_value"
        return {"message": "Redis connection test successful"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Redis connection test failed: {str(e)}",
        )
