from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import (
    List,
    Optional,
)

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


class UserRole(str, Enum):
    GUEST = "Guest"
    PLAYER = "Player"
    ADMINISTRATOR = "Administrator"
    NANNY_MODERATOR = "NannyModerator"
    REGULAR_MODERATOR = "RegularModerator"
    SENIOR_MODERATOR = "SeniorModerator"


class Rating(BaseModel):
    model_config = ConfigDict(extra="forbid")
    enabled: bool
    quality: int
    quantity: int


class User(BaseModel):
    model_config = ConfigDict(extra="forbid")
    login: str
    roles: List[UserRole]
    medium_picture_url: str = Field(None, alias='mediumPictureUrl')
    small_picture_url: str = Field(None, alias='smallPictureUrl')
    status: str = Field(None)
    rating: Rating
    online: datetime = Field(None)
    name: str = Field(None)
    location: str = Field(None)
    registration: datetime = Field(None)


class Metadata(BaseModel):
    email: str


class UserEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")
    resource: Optional[User] = None
    metadata: Optional[Metadata] = None
