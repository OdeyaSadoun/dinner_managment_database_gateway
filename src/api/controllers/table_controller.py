from typing import Any
from bson import ObjectId
import pymongo
from pymongo.errors import DuplicateKeyError

from globals.consts.data_errors_messages_const_strings import DataErrorsMessagesConstStrings
from globals.consts.database_const_strings import DatabaseConstStrings
from globals.consts.data_const_strings import DataConstStrings
from globals.consts.zmq_const_strings import ZMQConstStrings
from globals.enums.response_status import ResponseStatus
from infrastructures.interfaces.idatabase_manager import IDatabaseManager
from infrastructures.utils.serialization_util import SerializationUtil
from models.data_models.person_model import PersonModel
from models.data_models.table_model import TableModel
from models.data_classes.zmq_response import Response


class TableController:
    def __init__(self, database_manager: IDatabaseManager) -> None:
        self.collection = database_manager.db[DatabaseConstStrings.tables_collection]
        # self._ensure_indexes_creation()

    def import_tables_from_csv(self, tables: list) -> Response:
        try:
            if not tables:
                return Response(
                    status=ResponseStatus.ERROR,
                    data={ZMQConstStrings.error_message: "הרשימה ריקה"}
                )
            print("tables", len(tables))
            inserted_tables = []
            for table in tables:
                validated_table = TableModel(**table)
                table_data_to_insert = validated_table.dict(
                    by_alias=True, exclude_unset=False, exclude_none=False
                )

                result = self._handle_db_operation(
                    self.collection.insert_one, table_data_to_insert
                )

                inserted_tables.append({
                    "id": str(result.inserted_id),
                    "table_number": validated_table.table_number,
                    "chairs": validated_table.chairs,
                    "shape": validated_table.shape,
                    "gender": validated_table.gender,
                    "position": validated_table.position,
                    "people_list": validated_table.people_list,
                })
            print("inserted_tables", len(inserted_tables))

            return Response(
                status=ResponseStatus.SUCCESS,
                data={"tables": inserted_tables}
            )

        except Exception as e:
            return Response(
                status=ResponseStatus.ERROR,
                data={ZMQConstStrings.error_message: str(e)}
            )

    def get_table_by_id(self, table_id: str) -> Response:
        try:
            table = self._handle_db_operation(self.collection.find_one, {
                DataConstStrings.id_key: ObjectId(table_id),
                DataConstStrings.is_active_key: True
            })
            if not table:
                return Response(
                    status=ResponseStatus.ERROR,
                    data={
                        ZMQConstStrings.error_message: DataErrorsMessagesConstStrings.table_id_not_found_exception}
                )
            return Response(
                status=ResponseStatus.SUCCESS,
                data={
                    DataConstStrings.table_key: SerializationUtil.serialize_mongo_object(table)}
            )
        except Exception as e:
            return Response(
                status=ResponseStatus.ERROR,
                data={ZMQConstStrings.error_message: str(e)}
            )

    def get_all_tables(self) -> Response:
        try:
            tables = self._handle_db_operation(
                self.collection.find, {DataConstStrings.is_active_key: True})
            return Response(
                status=ResponseStatus.SUCCESS,
                data={DataConstStrings.tables_key: SerializationUtil.serialize_mongo_object(
                    list(tables))}
            )
        except Exception as e:
            return Response(
                status=ResponseStatus.ERROR,
                data={ZMQConstStrings.error_message: str(e)}
            )

    def create_table(self, table: TableModel) -> Response:
        try:
            print("create table db ctrl")
            validated_table = TableModel(**table)
            table_data = validated_table.dict(
                by_alias=True, exclude_none=True, exclude_unset=False
            )
            print("table_data", table_data)
            # בדיקה אם כבר קיים שולחן עם אותו מספר פעיל
            existing_table = self.collection.find_one({
                "table_number": table_data["table_number"],
                DataConstStrings.is_active_key: True
            })
            print("existing_table", existing_table)
            if existing_table:
                return Response(
                    status=ResponseStatus.ERROR,
                    data={
                        ZMQConstStrings.error_message: "שולחן עם מספר זה כבר קיים במערכת."
                    }
                )
            print("table not exist")
            existing_not_active_table = self.collection.find_one({
                "table_number": table_data["table_number"],
                DataConstStrings.is_active_key: False
            })
            print("existing_not_active_table", existing_not_active_table)
            if existing_not_active_table:
                table["is_active"] = True
                result = self._handle_db_operation(
                    self.collection.update_one,
                    {DataConstStrings.id_key: 
                        existing_not_active_table["_id"]},
                    {DatabaseConstStrings.set_operator: table}
                )
                if result.modified_count == 0:
                    return Response(
                        status=ResponseStatus.ERROR,
                        data={
                            ZMQConstStrings.error_message: DataErrorsMessagesConstStrings.update_table_exception}
                    )
                return Response(
                status=ResponseStatus.SUCCESS,
                data={DataConstStrings.inserted_id_key: str( existing_not_active_table["_id"])}
            )
            
            # הוספת שולחן חדש
            result = self.collection.insert_one(table_data)
            return Response(
                status=ResponseStatus.SUCCESS,
                data={DataConstStrings.inserted_id_key: str(result.inserted_id)}
            )

        except Exception as e:
            return Response(
                status=ResponseStatus.ERROR,
                data={ZMQConstStrings.error_message: str(e)}
            )

    def update_table_position(self, table_id: str, position: dict) -> Response:
        result = self._handle_db_operation(
            self.collection.update_one,
            {DataConstStrings.id_key: ObjectId(table_id), DataConstStrings.is_active_key: True},
            {DatabaseConstStrings.set_operator: {"position": position}}
        )
        if result.modified_count == 0:
            return Response(
                status=ResponseStatus.ERROR,
                data={ZMQConstStrings.error_message: "Failed to update position"}
            )
        return Response(status=ResponseStatus.SUCCESS)
            
    def remove_person_from_table(self, table_id: str, person_id: str) -> Response:
        result = self._handle_db_operation(
            self.collection.update_one,
            {DataConstStrings.id_key: ObjectId(table_id), DataConstStrings.is_active_key: True},
            {DatabaseConstStrings.pull_operator: {"people_list": ObjectId(person_id)}}
        )
        if result.modified_count == 0:
            return Response(
                status=ResponseStatus.ERROR,
                data={ZMQConstStrings.error_message: "Failed to remove person from table"}
            )
        return Response(status=ResponseStatus.SUCCESS)

    def add_person_to_table(self, table_id: str, person_id: str) -> Response:
        result = self._handle_db_operation(
            self.collection.update_one,
            {DataConstStrings.id_key: ObjectId(table_id), DataConstStrings.is_active_key: True},
            {DatabaseConstStrings.push_operator: {"people_list": ObjectId(person_id)}}
        )
        if result.modified_count == 0:
            return Response(
                status=ResponseStatus.ERROR,
                data={ZMQConstStrings.error_message: "Failed to add person to table"}
            )
        return Response(status=ResponseStatus.SUCCESS)

    def update_table(self, table_id: str, table: TableModel) -> None:
        try:
            validated_table = TableModel(**table)
            table_data_to_update = validated_table.dict(
                by_alias=True, exclude_none=True, exclude_unset=False)
            table_data_to_update.pop(DataConstStrings.id_key, None)
            result = self._handle_db_operation(
                self.collection.update_one,
                {DataConstStrings.id_key: ObjectId(
                    table_id), DataConstStrings.is_active_key: True},
                {DatabaseConstStrings.set_operator: table_data_to_update}
            )
            if result.modified_count == 0:
                return Response(
                    status=ResponseStatus.ERROR,
                    data={
                        ZMQConstStrings.error_message: DataErrorsMessagesConstStrings.update_table_exception}
                )
            return Response(
                status=ResponseStatus.SUCCESS
            )
        except Exception as e:
            return Response(
                status=ResponseStatus.ERROR,
                data={ZMQConstStrings.error_message: str(e)}
            )

    def delete_table(self, table_id: str) -> None:
        try:
            result = self._handle_db_operation(
                self.collection.update_one,
                {DataConstStrings.id_key: ObjectId(
                    table_id), DataConstStrings.is_active_key: True},
                {DatabaseConstStrings.set_operator: {
                    DataConstStrings.is_active_key: False}}
            )
            if not result.modified_count:
                return Response(
                    status=ResponseStatus.ERROR,
                    data={
                        ZMQConstStrings.error_message: DataErrorsMessagesConstStrings.table_id_not_found_exception}
                )
            return Response(
                status=ResponseStatus.SUCCESS
            )
        except Exception as e:
            return Response(
                status=ResponseStatus.ERROR,
                data={ZMQConstStrings.error_message: str(e)}
            )

    def _handle_db_operation(self, operation, *args, **kwargs) -> Any:
        try:
            return operation(*args, **kwargs)
        except DuplicateKeyError:
            raise ValueError(
                DataErrorsMessagesConstStrings.table_duplicate_key_exception)
        except Exception as e:
            raise Exception(
                f"{DataErrorsMessagesConstStrings.general_exception} {e}")
