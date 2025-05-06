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
            ZMQConstStrings.get_all_users: self.get_all_users,
            ZMQConstStrings.get_user_by_id: self.get_user_by_id,
            ZMQConstStrings.get_user_by_username_and_password: self.get_user_by_username_and_password,
            ZMQConstStrings.delete_user: self.delete_user,
            ZMQConstStrings.update_user: self.update_user,
        }

    def register(self, data: Any) -> Response:
        user = data.get(DataConstStrings.user_key)
        return self._ctrl.register(user)

    def login(self, data: Any) -> Response:
        user = data.get(DataConstStrings.user_key)
        return self._ctrl.login(user)

    def get_all_users(self, data: Any) -> Response:
        return self._ctrl.get_all_users()

    def get_user_by_id(self, data: Any) -> Response:
        user_id = data.get(DataConstStrings.user_id_key)
        return self._ctrl.get_user_by_id(user_id)
    
    def get_user_by_username_and_password(self, data: Any) -> Response:
        username = data.get(DataConstStrings.username_key)
        password = data.get(DataConstStrings.password_key)
        return self._ctrl.get_user_by_username_and_password(username, password)

    def delete_user(self, data: Any) -> Response:
        user_id = data.get(DataConstStrings.user_id_key)
        return self._ctrl.delete_user(user_id)

    def update_user(self, data: Any) -> Response:
        user_id = data.get(DataConstStrings.user_id_key)
        updated_user_data = data.get(DataConstStrings.user_data_key)
        return self._ctrl.update_user(user_id, updated_user_data)
