from bson import ObjectId
from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Optional, Tuple

from api.validators.person_validators import PersonValidators 
from models.data_models.person_model import PersonModel
from globals.consts.const_strings import ConstStrings
from dinner_managment_database_gateway.src.globals.consts.data_const_strings import PersonDataConstStrings


class TableModel(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias=ConstStrings.id_before_serialization) 
    people_list: List[PersonModel] = Field(...)
    is_active: bool = Field(default=True)
    date_created: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat(),
        }