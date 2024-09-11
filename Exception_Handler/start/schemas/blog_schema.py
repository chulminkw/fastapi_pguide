from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Annotated
from pydantic.dataclasses import dataclass

class BlogInput(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    author: str = Field(..., max_length=100)
    content: str = Field(..., min_length=2, max_length=4000)
    image_loc: Optional[str] = Field(None, max_length=400)
    #image_loc: Annotated[str, Field(None, max_length=400)] = None

class Blog(BlogInput):
    id: int
    modified_dt: datetime

@dataclass
class BlogData:
    id: int
    title: str
    author: str
    content: str
    modified_dt: datetime
    image_loc: str | None = None