from fastapi import FastAPI
from .dependencies import create_db_and_tables
from .routers import heroes


app = FastAPI()

app.include_router(heroes.router)


# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()


@app.get(
    "/",
    response_model=dict[str, str],
    responses={
        200: {
            "description": "Test if the server is available",
            "content": {
                "application/json": {"example": {"message": "The server is running!"}}
            },
        }
    },
)
async def health_check():
    return {"message": "The server is running!"}
