from typing import Any
from api.routers.base_router import BaseRouter

from models.data_classes.zmq_response import Response
from infrastructures.interfaces.icontroller_manager import IControllerManager
from globals.consts.data_const_strings import DataConstStrings
from globals.consts.zmq_const_strings import ZMQConstStrings


class UserRouter(BaseRouter):
    def __init__(self, resource: str, ctrl: IControllerManager) -> None:
        super().__init__(resource, ctrl)
        self._setup_operations()

    def _setup_operations(self):
        self._operations = {
            ZMQConstStrings.register: self.register,
            ZMQConstStrings.login: self.login,
        }

    def register(self, data: Any) -> Response:
        user = data.get(DataConstStrings.user_key)
        return self._ctrl.register(user)

    def login(self, data: Any) -> Response:
        user = data.get(DataConstStrings.user_key)
        return self._ctrl.login(user)
