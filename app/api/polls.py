from uuid import UUID
from fastapi import APIRouter, HTTPException

from app.models.Polls import PollCreate
from app.services import utils

router = APIRouter()


@router.post("/create")
def create_poll(poll: PollCreate):
    new_poll = poll.create_poll()

    utils.save_poll(new_poll)

    return {
        "detail": "Poll successfully created",
        "poll_id": new_poll.id,
        "poll": new_poll,
    }


@router.get("/{poll_id}")
def get_poll(poll_id: UUID):
    poll = utils.get_poll(poll_id)

    if not poll:
        raise HTTPException(status_code=404, detail="A poll by that id was not found")

    return poll


@router.get("/")
def get_polls():
    polls = utils.get_all_polls()

    if not polls:
        raise HTTPException(status_code=404, detail="No polls where found")

    return polls
