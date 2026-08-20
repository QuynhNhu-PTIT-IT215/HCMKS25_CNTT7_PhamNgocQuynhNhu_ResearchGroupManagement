from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

from app.db.database import Base, engine
from app.models.user import User
from app.models.research_project import ResearchProject, ResearchMember
from app.models.research_task import ResearchTask

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def test():
    return {
        "message": "Server đang hoạt động"
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail
        }
    )