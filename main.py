from fastapi import FastAPI
from upstash_redis import Redis
from dotenv import load_dotenv
import os
from app.models.Polls import Poll, PollCreate

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")
REDIS_TOKEN = os.getenv("REDIS_TOKEN")

app = FastAPI()


@app.get("/test")
def test():
    return {"message": "Hello there"}


@app.post("/polls/create")
def create_poll(poll: PollCreate):

    # return Poll(title="Some placeholder title", options=["yes", "no", "maybe"])
    new_poll = poll.create_poll()
    return {"detail": "Poll successfully created", "poll_id": new_poll.poll_id}


redis_client = Redis(url=REDIS_URL, token=REDIS_TOKEN)


@app.post("/redis/save", tags=["throwaway"])
def save_redis(id: str, name: str):
    redis_client.set(id, name)
    return {"status": "success"}


@app.get("/redis/get/{id}", tags=["throwaway"])
def get_redis(id: str):
    name = redis_client.get(id)
    return {"id": id, "name": name}
