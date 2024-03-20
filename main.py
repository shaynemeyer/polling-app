from fastapi import FastAPI

from app.models.Polls import Poll, PollCreate

app = FastAPI()


@app.get("/test")
def test():
    return {"message": "Hello there"}


@app.post("/polls/create")
def create_poll(poll: PollCreate):

    # return Poll(title="Some placeholder title", options=["yes", "no", "maybe"])
    new_poll = poll.create_poll()
    return {"detail": "Poll successfully created", "poll_id": new_poll.poll_id}
