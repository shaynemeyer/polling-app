from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class ChoiceCreate(BaseModel):
    """Choice write data model, representing a single choice in a poll"""

    description: str = Field(min_length=1, max_length=100)


class Choice(ChoiceCreate):
    """Choice read data model, with a label and auto-generated uuid"""

    id: UUID = Field(default_factory=uuid4)
    label: int = Field(gte=1, lte=5)
