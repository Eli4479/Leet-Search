from pydantic import BaseModel, Field
from typing import List


class Problem(BaseModel):
    id: str
    title: str
    url: str
    tags: List[str]
    content: str
    original_content: str
    match_percentage: float

    class Config:
        validate_by_name = True
