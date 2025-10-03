import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from logger import logger

from app.core.config import settings
from app.routers import healthcheck
from app.routers import users
from app.routers import companies
from app.routers import auth
from app.routers import membership
from app.routers import quizzes
from app.routers import quiz_result
from app.routers import export_data


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(companies.router)
app.include_router(membership.router)
app.include_router(healthcheck.router)
app.include_router(quizzes.router)
app.include_router(quiz_result.router)
app.include_router(export_data.router)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.app.HOST,
        port=settings.app.PORT,
        reload=settings.app.RELOAD,
    )
