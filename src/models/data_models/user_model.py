from bson import ObjectId
from datetime import datetime, timezone
from typing import Literal, Optional
from pydantic import BaseModel, Field

from globals.consts.const_strings import ConstStrings


class UserModel(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias=ConstStrings.id_before_serialization) 
    name: str = Field(...)
    username: str = Field(...)
    password: str = Field(...)
    role: Literal["admin", "user"] = "user"
    is_active: bool = Field(default=True)
    date_created: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat(),
        }