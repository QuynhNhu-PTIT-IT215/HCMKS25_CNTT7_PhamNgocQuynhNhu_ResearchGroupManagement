from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.routers import users
from app.routers import research_project, research_task
from app.routers import auth

from app.models.user import User
from app.models.research_project import ResearchProject, ResearchMember
from app.models.research_task import ResearchTask
from app.models.history import History

from app.db.database import Base, engine


Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(users.router)
app.include_router(research_task.router)
app.include_router(research_project.router)
app.include_router(auth.router)


@app.get("/health")
def health_check():
    return {
        "success": True,
        "message": "Server đang hoạt động"
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "status_code": exc.status_code,
            "message": exc.detail
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "status_code": 422,
            "message": "Dữ liệu đầu vào không hợp lệ"
        }
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(
    request: Request,
    exc: IntegrityError
):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "status_code": 400,
            "message": "Dữ liệu không hợp lệ hoặc bị trùng"
        }
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(
    request: Request,
    exc: SQLAlchemyError
):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "status_code": 400,
            "message": "Không thể xử lý dữ liệu trong cơ sở dữ liệu"
        }
    )