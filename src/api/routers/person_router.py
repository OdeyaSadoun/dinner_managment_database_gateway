from typing import Any
from api.routers.base_router import BaseRouter
from models.data_classes.zmq_response import Response
from infrastructures.interfaces.icontroller_manager import IControllerManager
from globals.consts.data_const_strings import DataConstStrings
from globals.consts.zmq_const_strings import ZMQConstStrings


class PersonRouter(BaseRouter):
    def __init__(self, resource: str, ctrl: IControllerManager) -> None:
        super().__init__(resource, ctrl)
        self._setup_operations()

    def _setup_operations(self) -> None:
        self._operations = {
            ZMQConstStrings.get_all_people: self.get_all_people,
            ZMQConstStrings.get_person_by_id: self.get_person_by_id,
            ZMQConstStrings.create_person: self.create_person,
            ZMQConstStrings.update_person: self.update_person,
            ZMQConstStrings.seat_person: self.seat_person,
            ZMQConstStrings.unseat_person: self.unseat_person,
            ZMQConstStrings.delete_person: self.delete_person,
        }

    def get_all_people(self, data: Any = None) -> Response:
        return self._ctrl.get_all_people()

    def get_person_by_id(self, data: Any) -> Response:
        person_id = data.get(DataConstStrings.person_id_key)
        return self._ctrl.get_person_by_id(person_id)

    def create_person(self, data: Any) -> Response:
        person = data.get(DataConstStrings.person_key)
        return self._ctrl.create_person(person)

    def update_person(self, data: Any) -> Response:
        person_id = data.get(DataConstStrings.person_id_key)
        person = data.get(DataConstStrings.person_key)
        return self._ctrl.update_person(person_id, person)

    def seat_person(self, data: Any) -> Response:
        person_id = data.get(DataConstStrings.person_id_key)
        return self._ctrl.seat_person(person_id)    

    def unseat_person(self, data: Any) -> Response:
        person_id = data.get(DataConstStrings.person_id_key)
        return self._ctrl.unseat_person(person_id)

    def delete_person(self, data: Any) -> Response:
        person_id = data.get(DataConstStrings.person_id_key)
        return self._ctrl.delete_person(person_id)
