from bson import ObjectId
from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Literal, Optional, Tuple

from api.validators.person_validators import PersonValidators 
from globals.consts.const_strings import ConstStrings
from globals.consts.data_const_strings import DataConstStrings


class PersonModel(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias=ConstStrings.id_before_serialization) 
    name: str = Field(...)
    phone: str = Field(...)
    table_number: int = Field(...)
    is_reach_the_dinner: bool = Field(...)
    gender: Literal["male", "female"]
    contact_person: str
    add_manual: bool
    is_active: bool = Field(default=True)
    date_created: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator(DataConstStrings.phone_key)
    def validate_phone(cls, value):
        return PersonValidators.validate_phone(value)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat(),
        }