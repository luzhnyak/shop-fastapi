from functools import wraps
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.core.exceptions import ConflictException, DatabaseException


def db_error_handler(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except IntegrityError as e:
            await self.session.rollback()
            raise ConflictException(
                str(e.orig) if e.orig else "Integrity constraint error"
            )
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(str(e))

    return wrapper
