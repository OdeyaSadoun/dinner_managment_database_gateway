import json
from typing import Dict

from globals.enums.response_status import ResponseStatus
from globals.consts.zmq_const_strings import ZMQConstStrings


class Response:
    def __init__(self, status: ResponseStatus, data: Dict = {}):
        self.status = status
        self.data = data

    def to_json(self):
        return json.dumps({
            ZMQConstStrings.status_identifier: self.status.name,
            ZMQConstStrings.data_identifier: self.data
        })

    @classmethod
    def from_json(self, json_str: str):
        json_dict = json.loads(json_str)
        status = ResponseStatus[json_dict[ZMQConstStrings.status_identifier]]
        data = json_dict.get(ZMQConstStrings.data_identifier, {})
        return self(status=status, data=data)

    status: ResponseStatus
    data: Dict