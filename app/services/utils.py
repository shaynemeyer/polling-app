from upstash_redis import Redis
from dotenv import load_dotenv
from uuid import UUID
from typing import Optional
import os

from app.models.Polls import Poll

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


def get_choice_id_by_label(poll_id: UUID, label: int) -> Optional[UUID]:
    poll = get_poll(poll_id)

    if not poll:
        return None

    for choice in poll.options:
        if choice.label == label:
            return choice.id

    return None
