from bson import ObjectId
from datetime import datetime

from globals.consts.const_strings import ConstStrings

class SerializationUtil:
    @staticmethod
    def serialize_mongo_object(obj):
        if isinstance(obj, list):
            return [SerializationUtil.serialize_mongo_object(item) for item in obj]
        if isinstance(obj, dict):
            serialized_dict = {}
            for key, value in obj.items():
                if key == ConstStrings.id_before_serialization:
                    serialized_dict[ConstStrings.id_after_serialization] = SerializationUtil.serialize_mongo_object(value)
                else:
                    serialized_dict[key] = SerializationUtil.serialize_mongo_object(value)
            return serialized_dict
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return obj