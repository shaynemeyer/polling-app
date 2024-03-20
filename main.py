from fastapi import FastAPI
from app.api import polls


app = FastAPI()

app.include_router(polls.router, prefix="/polls", tags=["polls"])


@app.get("/test")
def test():
    return {"message": "Hello there"}
