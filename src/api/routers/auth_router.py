from api.routers.base_router import BaseRouter
from infrastructures.interfaces.icontroller_manager import IControllerManager
from globals.consts.data_const_strings import DataConstStrings
from globals.consts.zmq_const_strings import ZMQConstStrings


class AutnRouter(BaseRouter):
    def __init__(self, resource: str, ctrl: IControllerManager):
        super().__init__(resource, ctrl)
        self._setup_operations()

    def _setup_operations(self):
        self._operations = {
            ZMQConstStrings.register: self.register,
            ZMQConstStrings.login: self.login,
        }

    def register(self, data):
        username = data.get(DataConstStrings.username_key)
        email = data.get(DataConstStrings.email_key)
        password = data.get(DataConstStrings.password_key)
        return self._ctrl.create_table(username, email, password)

    def login(self, data):
        email = data.get(DataConstStrings.email_key)
        password = data.get(DataConstStrings.password_key)
        return self._ctrl.create_table(email, password)
