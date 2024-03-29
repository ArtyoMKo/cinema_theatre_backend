"""
Cinema back-end application.

This project supposed to organize cinema application back end.
Endpoints with authorization requirement supposed to be used for
"""
from fastapi import FastAPI
from starlette.responses import JSONResponse
from starlette.requests import Request

from cinema_application.database import engine
from cinema_application.routers import rooms, auth, movies, movie_sessions, reservations
from cinema_application import models

app = FastAPI(
    title="Cinema theatre back-end application",
    description="""
    Cinema theatre back-end application.
    
    Application created for managing cinema theatre movie sessions organization.
    
    You will be able to create admins, add/delete/update movies, rooms, movie sessions, manage session reservations, 
    etc. 
    
    Good luck !
    """,
)

models.Base.metadata.create_all(bind=engine)
app.include_router(rooms.router)
app.include_router(auth.router)
app.include_router(movies.router)
app.include_router(movie_sessions.router)
app.include_router(reservations.router)


@app.exception_handler(Exception)
async def exception_handler(
    request: Request, exc: Exception
):  # pylint: disable=unused-argument
    return JSONResponse(
        status_code=500,
        content={"message": f"Oops!. Internal server error with message {exc}"},
    )
