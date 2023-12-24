from typing import Optional

from pydantic import BaseModel, EmailStr, AnyUrl, PositiveInt, field_validator, ValidationInfo

class TVEpisode(BaseModel):
    id: Optional[PositiveInt] = None
    name: Optional[str] = None
    season: Optional[int] = None
    number: Optional[int] = None
    type: Optional[str] = None
    airdate: Optional[str] = None
    airtime: Optional[str] = None
    airstamp: Optional[str] = None
    runtime: Optional[int] = None
    rating_average: Optional[float] = None
    summary: Optional[str] = None
    likes: Optional[int] = None