from typing import List

from pydantic import BaseModel


class Observation(BaseModel):
    code_snippet: str
    language: str
    task_name: str
    max_steps: int
    current_step: int
    snippet_id: str


class Action(BaseModel):
    review: str


class Reward(BaseModel):
    score: float
    issues_found: List[dict]
    issues_missed: List[dict]
    feedback: str
