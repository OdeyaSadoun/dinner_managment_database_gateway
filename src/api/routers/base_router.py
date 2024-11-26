from infrastructures.interfaces.icontroller_manager import IControllerManager
from globals.consts.zmq_const_strings import ZMQConstStrings
from globals.enums.response_status import ResponseStatus
from models.data_classes.zmq_response import Response


class BaseRouter:
    def __init__(self, resource: str, ctrl: IControllerManager) -> None:
        self.resource = resource
        self._ctrl = ctrl
        self._operations = {}
        self._setup_operations()

    def _setup_operations(self):
        pass

    def handle_operation(self, operation, data):
        if operation in self._operations:
            return self._operations[operation](data)
        else:
            return Response(
                status=ResponseStatus.ERROR,
                data={
                    ZMQConstStrings.error_message: ZMQConstStrings.unknown_operation_error_message}
            )
