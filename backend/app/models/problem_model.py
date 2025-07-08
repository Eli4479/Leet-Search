from pydantic import BaseModel, Field
from typing import Optional
from typing import List


class Problem(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    url: Optional[str] = None
    content: Optional[str] = None
    original_content: Optional[str] = None
    match_percentage: Optional[float] = None

    class Config:
        validate_by_name = True
