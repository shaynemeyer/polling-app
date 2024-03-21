from upstash_redis import Redis
from dotenv import load_dotenv
from uuid import UUID
from typing import List, Optional
import os

from app.models.Polls import Poll
from app.models.Votes import Vote

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")
REDIS_TOKEN = os.getenv("REDIS_TOKEN")

redis_client = Redis(url=REDIS_URL, token=REDIS_TOKEN)


def save_poll(poll: Poll):
    poll_json = poll.model_dump_json()
    redis_client.set(f"poll:{poll.id}", poll_json)


def get_poll(poll_id: UUID) -> Optional[Poll]:
    poll_json = redis_client.get(f"poll:{poll_id}")

    if poll_json:
        return Poll.model_validate_json(poll_json)

    return None


def get_all_polls() -> List[Poll]:
    poll_keys = redis_client.keys("poll:*")
    polls = []

    for key in poll_keys:
        poll_json = redis_client.get(key)
        if poll_json:
            polls.append(Poll.model_validate_json(poll_json))

    return polls


def get_choice_id_by_label(poll_id: UUID, label: int) -> Optional[UUID]:
    poll = get_poll(poll_id)

    return get_choice_id_by_label_given_poll(poll, label)


def get_choice_id_by_label_given_poll(poll: Poll, label: int) -> Optional[UUID]:
    if not poll:
        return None

    for choice in poll.options:
        if choice.label == label:
            return choice.id

    return None


def get_vote(poll_id: UUID, email: str) -> Optional[Vote]:
    vote_json = redis_client.hget(f"votes:{poll_id}", email)

    if vote_json:
        return Vote.model_validate_json(vote_json)

    return None


def save_vote(poll_id: UUID, vote: Vote) -> None:
    vote_json = vote.model_dump_json()
    redis_client.hset(f"votes:{poll_id}", vote.voter.email, vote_json)
