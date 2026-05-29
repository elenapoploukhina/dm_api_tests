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

from dm_api_account.models.user_envelope import (
    UserRole,
    Rating,
)


class BbParseMode(str, Enum):
    COMMON = "Common"
    INFO = "Info"
    POST = "Post"
    CHAT = "Chat"


class ColorSchema(str, Enum):
    MODERN = "Modern"
    PALE = "Pale"
    CLASSIC = "Classic"
    Classic_PALE = "ClassicPale"
    NIGHT = "Night"


class InfoBbText(BaseModel):
    model_config = ConfigDict(extra="forbid")
    value: str
    parse_mode: BbParseMode = Field(..., alias='parseMode')


class PagingSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")
    posts_per_page: int = Field(..., alias='postsPerPage')
    comments_per_page: int = Field(..., alias='commentsPerPage')
    topics_per_page: int = Field(..., alias='topicsPerPage')
    messages_per_page: int = Field(..., alias='messagesPerPage')
    entities_per_page: int = Field(..., alias='entitiesPerPage')


class UserSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")
    color_schema: ColorSchema = Field(..., alias='colorSchema')
    nanny_greetings_message: str = Field(None, alias='nannyGreetingsMessage')
    paging: PagingSettings


class UserDetails(BaseModel):
    model_config = ConfigDict(extra="forbid")
    login: str
    roles: List[UserRole]
    medium_picture_url: str = Field(None, alias='mediumPictureUrl')
    small_picture_url: str = Field(None, alias='smallPictureUrl')
    status: str = None
    rating: Rating
    online: datetime
    name: str = None
    location: str = None
    registration: datetime
    icq: str = None
    skype: str = None
    original_picture_url: str = Field(None, alias='originalPictureUrl')
    info: InfoBbText | str = Field(None)
    settings: UserSettings


class UserDetailsEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")
    resource: Optional[UserDetails] = None
    metadata: Optional[str] = None
