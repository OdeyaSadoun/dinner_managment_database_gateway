import json
from typing import Dict

from globals.consts.zmq_const_strings import ZMQConstStrings


class Request:
    def __init__(self, resource: str, operation: str, data: Dict = {}):
        self.resource = resource
        self.operation = operation
        self.data = data

    def to_json(self):
        return json.dumps({
            ZMQConstStrings.resource_identifier: self.resource,
            ZMQConstStrings.operation_identifier: self.operation,
            ZMQConstStrings.data_identifier: self.data
        })
    
    @classmethod
    def from_json(self, json_str: str):
        request = json.loads(json_str)
        return self(resource=request[ZMQConstStrings.resource_identifier], 
                    operation=request[ZMQConstStrings.operation_identifier], 
                    data=request.get(ZMQConstStrings.data_identifier, {}))
    
    resource: str
    operation: str
    data: Dict