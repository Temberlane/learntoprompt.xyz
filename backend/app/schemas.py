from pydantic import BaseModel
from datetime import datetime


class PromptBase(BaseModel):
    title: str
    content: str


class PromptCreate(PromptBase):
    pass


class PromptRead(PromptBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
