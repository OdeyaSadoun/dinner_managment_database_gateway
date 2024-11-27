from bson import ObjectId
from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field

from globals.consts.const_strings import ConstStrings


class AuthModel(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias=ConstStrings.id_before_serialization) 
    username: str
    password: str
    is_active: bool = Field(default=True)
    date_created: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat(),
        }