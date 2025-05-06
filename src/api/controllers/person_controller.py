from typing import Any
from bson import ObjectId
import pymongo
from pymongo.errors import DuplicateKeyError

from globals.consts.data_errors_messages_const_strings import DataErrorsMessagesConstStrings
from globals.consts.database_const_strings import DatabaseConstStrings
from globals.consts.data_const_strings import DataConstStrings
from globals.consts.zmq_const_strings import ZMQConstStrings
from infrastructures.interfaces.idatabase_manager import IDatabaseManager
from infrastructures.utils.serialization_util import SerializationUtil
from models.data_models.person_model import PersonModel
from models.data_classes.zmq_response import Response
from globals.enums.response_status import ResponseStatus


class PersonController:
    def __init__(self, database_manager: IDatabaseManager) -> None:
        self.collection = database_manager.db[DatabaseConstStrings.people_collection]
        # self._ensure_indexes_creation()

    def get_person_by_id(self, person_id: str) -> Response:
        try:
            person = self._handle_db_operation(self.collection.find_one, {
                DataConstStrings.id_key: ObjectId(person_id),
                DataConstStrings.is_active_key: True
            })
            if not person:
                return Response(
                    status=ResponseStatus.ERROR,
                    data={
                        ZMQConstStrings.error_message: DataErrorsMessagesConstStrings.person_id_not_found_exception}
                )
            return Response(
                status=ResponseStatus.SUCCESS,
                data={
                    DataConstStrings.person_key: SerializationUtil.serialize_mongo_object(person)}
            )
        except Exception as e:
            return Response(
                status=ResponseStatus.ERROR,
                data={ZMQConstStrings.error_message: str(e)}
            )

    def get_manual_people(self) -> Response:
        try:
            people = self._handle_db_operation(
                self.collection.find, {
                    DataConstStrings.is_active_key: True,
                    DataConstStrings.add_manual_key: True
                })
            return Response(
                status=ResponseStatus.SUCCESS,
                data={DataConstStrings.people_key: SerializationUtil.serialize_mongo_object(
                    list(people))}
            )
        except Exception as e:
            return Response(
                status=ResponseStatus.ERROR,
                data={ZMQConstStrings.error_message: str(e)}
            )

    def get_all_people(self) -> Response:
        try:
            people = self._handle_db_operation(
                self.collection.find, {DataConstStrings.is_active_key: True})
            return Response(
                status=ResponseStatus.SUCCESS,
                data={DataConstStrings.people_key: SerializationUtil.serialize_mongo_object(
                    list(people))}
            )
        except Exception as e:
            return Response(
                status=ResponseStatus.ERROR,
                data={ZMQConstStrings.error_message: str(e)}
            )

    def create_person(self, person: PersonModel) -> None:
        try:
            print("person", person)
            validated_person = PersonModel(**person)
            print("validated_person", validated_person)
            person_data_to_insert = validated_person.dict(
                by_alias=True, exclude_none=True, exclude_unset=False)
            result = self._handle_db_operation(
                self.collection.insert_one, person_data_to_insert)
            return Response(
                status=ResponseStatus.SUCCESS,
                data={DataConstStrings.id_key: str(result.inserted_id),
                      "name": validated_person.name,
                      "phone": validated_person.phone,
                      "table_number": validated_person.table_number,
                      "add_manual": validated_person.add_manual,
                      "gender": validated_person.gender,
                      "contact_person": validated_person.contact_person,
                      "is_reach_the_dinner": validated_person.is_reach_the_dinner
                      }
            )
        except Exception as e:
            return Response(
                status=ResponseStatus.ERROR,
                data={ZMQConstStrings.error_message: str(e)}
            )

    def update_person(self, person_id: str, person: PersonModel) -> None:
        try:
            validated_person = PersonModel(**person)
            person_data_to_update = validated_person.dict(
                by_alias=True, exclude_none=True, exclude_unset=False)
            person_data_to_update.pop(DataConstStrings.id_key, None)
            result = self._handle_db_operation(
                self.collection.update_one,
                {DataConstStrings.id_key: ObjectId(
                    person_id), DataConstStrings.is_active_key: True},
                {DatabaseConstStrings.set_operator: person_data_to_update}
            )
            if result.modified_count == 0:
                return Response(
                    status=ResponseStatus.ERROR,
                    data={
                        ZMQConstStrings.error_message: DataErrorsMessagesConstStrings.update_person_exception}
                )
            return Response(
                status=ResponseStatus.SUCCESS
            )
        except Exception as e:
            return Response(
                status=ResponseStatus.ERROR,
                data={ZMQConstStrings.error_message: str(e)}
            )

    def seat_person(self, person_id: str) -> None:
        try:
            result = self._handle_db_operation(
                self.collection.update_one,
                {DataConstStrings.id_key: ObjectId(
                    person_id), DataConstStrings.is_active_key: True},
                {DatabaseConstStrings.set_operator: {
                    DataConstStrings.is_reach_the_dinner_key: True}}
            )
            if result.modified_count == 0:
                return Response(
                    status=ResponseStatus.ERROR,
                    data={
                        ZMQConstStrings.error_message: DataErrorsMessagesConstStrings.person_id_not_found_exception}
                )
            return Response(
                status=ResponseStatus.SUCCESS
            )
        except Exception as e:
            return Response(
                status=ResponseStatus.ERROR,
                data={ZMQConstStrings.error_message: str(e)}
            )

    def unseat_person(self, person_id: str) -> None:
        try:
            result = self._handle_db_operation(
                self.collection.update_one,
                {DataConstStrings.id_key: ObjectId(
                    person_id), DataConstStrings.is_active_key: True},
                {DatabaseConstStrings.set_operator: {
                    DataConstStrings.is_reach_the_dinner_key: False}}
            )
            if result.modified_count == 0:
                return Response(
                    status=ResponseStatus.ERROR,
                    data={
                        ZMQConstStrings.error_message: DataErrorsMessagesConstStrings.person_id_not_found_exception}
                )
            return Response(
                status=ResponseStatus.SUCCESS
            )
        except Exception as e:
            return Response(
                status=ResponseStatus.ERROR,
                data={ZMQConstStrings.error_message: str(e)}
            )

    def delete_person(self, person_id: str) -> None:
        try:
            result = self._handle_db_operation(
                self.collection.update_one,
                {DataConstStrings.id_key: ObjectId(
                    person_id), DataConstStrings.is_active_key: True},
                {DatabaseConstStrings.set_operator: {
                    DataConstStrings.is_active_key: False}}
            )
            if not result.modified_count:
                return Response(
                    status=ResponseStatus.ERROR,
                    data={
                        ZMQConstStrings.error_message: DataErrorsMessagesConstStrings.person_id_not_found_exception}
                )
            return Response(
                status=ResponseStatus.SUCCESS
            )
        except Exception as e:
            return Response(
                status=ResponseStatus.ERROR,
                data={ZMQConstStrings.error_message: str(e)}
            )

    # def _ensure_indexes_creation(self) -> None:
    #     existing_indexes = [index[DatabaseConstStrings.index_name] for index in self.collection.list_indexes()]
    #     indexes_to_ensure = [
    #         (DataConstStrings.personal_number, {DatabaseConstStrings.index_name: DatabaseConstStrings.personal_number_index, DatabaseConstStrings.unique_index: True})
    #     ]
    #     for field, options in indexes_to_ensure:
    #         if options[DatabaseConstStrings.index_name] not in existing_indexes:
    #             self.collection.create_index([(field, pymongo.ASCENDING)], **options)

    def _handle_db_operation(self, operation, *args, **kwargs) -> Any:
        try:
            return operation(*args, **kwargs)
        except DuplicateKeyError:
            raise ValueError(
                DataErrorsMessagesConstStrings.person_duplicate_key_exception)
        except Exception as e:
            raise Exception(
                f"{DataErrorsMessagesConstStrings.general_exception} {e}")
