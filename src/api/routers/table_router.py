from typing import Any

from api.routers.base_router import BaseRouter
from models.data_classes.zmq_response import Response
from infrastructures.interfaces.icontroller_manager import IControllerManager
from globals.consts.data_const_strings import DataConstStrings
from globals.consts.zmq_const_strings import ZMQConstStrings


class TableRouter(BaseRouter):
    def __init__(self, resource: str, ctrl: IControllerManager) -> None:
        super().__init__(resource, ctrl)
        self._setup_operations()

    def _setup_operations(self) -> None:
        self._operations = {
            ZMQConstStrings.get_all_tables: self.get_all_tables,
            ZMQConstStrings.get_table_by_id: self.get_table_by_id,
            ZMQConstStrings.create_table: self.create_table,
            ZMQConstStrings.update_table_position: self.update_table_position,
            ZMQConstStrings.update_table: self.update_table,
            ZMQConstStrings.delete_table: self.delete_table,
            ZMQConstStrings.add_person_to_table: self.add_person_to_table,
            ZMQConstStrings.remove_person_from_table: self.remove_person_from_table,
        }

    def get_all_tables(self, data: Any = None) -> Response:
        return self._ctrl.get_all_tables()

    def get_table_by_id(self, data: Any) -> Response:
        table_id = data.get(DataConstStrings.table_id_key)
        return self._ctrl.get_table_by_id(table_id)

    def create_table(self, data: Any) -> Response:
        table = data.get(DataConstStrings.table_key)
        return self._ctrl.create_table(table)

    def update_table(self, data: Any) -> Response:
        table_id = data.get(DataConstStrings.table_id_key)
        table = data.get(DataConstStrings.table_key)
        return self._ctrl.update_table(table_id, table)

    def update_table_position(self, data: Any) -> Response:
        table_id = data.get(DataConstStrings.table_id_key)
        position = data.get(DataConstStrings.position_key)
        print("position, router, db", position)
        return self._ctrl.update_table_position(table_id, position)

    def delete_table(self, data: Any) -> Response:
        table_id = data.get(DataConstStrings.table_id_key)
        return self._ctrl.delete_table(table_id)

    def add_person_to_table(self, data: Any) -> Response:
        table_id = data.get(DataConstStrings.table_id_key)
        person_id = data.get(DataConstStrings.person_id_key)
        return self._ctrl.add_person_to_table(table_id, person_id)
    
    def remove_person_from_table(self, data: Any) -> Response:
        table_id = data.get(DataConstStrings.table_id_key)
        person_id = data.get(DataConstStrings.person_id_key)
        return self._ctrl.remove_person_from_table(table_id, person_id)
