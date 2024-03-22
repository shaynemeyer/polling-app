from typing import List
from pydantic import BaseModel


class Result(BaseModel):
    description: str
    vote_count: int


class PollResults(BaseModel):
    title: str
    total_votes: int
    results: List[Result]
