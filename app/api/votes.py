from uuid import UUID
from fastapi import APIRouter, HTTPException

from app.models.Votes import VoteById, VoteByLabel, Vote, Voter
from app.services import utils

router = APIRouter()


@router.post("/{poll_id}/id")
def vote_by_id(poll_id: UUID, vote: VoteById):
    poll = utils.get_poll(poll_id)

    if not poll.is_active():
        raise HTTPException(status_code=400, detail="The poll has expired")

    if utils.get_vote(poll_id=poll_id, email=vote.voter.email):
        raise HTTPException(status_code=400, detail="Already voted")

    vote = Vote(
        poll_id=poll_id,
        choice_id=vote.choice_id,
        voter=Voter(
            **vote.voter.model_dump(),
        ),
    )

    utils.save_vote(poll_id=poll_id, vote=vote)

    return {"message": "Vote recorded", "vote": vote}


@router.post("/{poll_id}/label")
def vote_by_label(poll_id: UUID, vote: VoteByLabel):
    poll = utils.get_poll(poll_id)

    if not poll.is_active():
        raise HTTPException(status_code=400, detail="The poll has expired")

    if utils.get_vote(poll_id=poll_id, email=vote.voter.email):
        raise HTTPException(status_code=400, detail="Already voted")

    choice_id = utils.get_choice_id_by_label(poll_id, vote.choice_label)

    if not choice_id:
        raise HTTPException(status_code=400, detail="Invalid choice label provided")

    vote = Vote(
        poll_id=poll_id,
        choice_id=choice_id,
        voter=Voter(
            **vote.voter.model_dump(),
        ),
    )

    utils.save_vote(poll_id=poll_id, vote=vote)

    return {"message": "Vote recorded", "vote": vote}
