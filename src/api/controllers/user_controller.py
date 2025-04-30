import os
import jwt
import bcrypt
import datetime
from typing import Any, Dict
from pymongo.errors import DuplicateKeyError
from bson import ObjectId

from models.data_classes.login_user import LoginUser
from globals.consts.const_strings import ConstStrings
from globals.consts.data_errors_messages_const_strings import DataErrorsMessagesConstStrings
from globals.consts.data_const_strings import DataConstStrings
from globals.consts.zmq_const_strings import ZMQConstStrings
from globals.enums.response_status import ResponseStatus
from globals.consts.database_const_strings import DatabaseConstStrings
from infrastructures.interfaces.idatabase_manager import IDatabaseManager
from models.data_classes.zmq_response import Response
from models.data_models.user_model import UserModel


class UserController:
    def __init__(self, database_manager: IDatabaseManager) -> None:
        self.collection = database_manager.db[DatabaseConstStrings.users_collection]

    def register(self, user: UserModel) -> Response:
        try:
            validated_user = UserModel(**user)
            existing_user = self._handle_db_operation(
                self.collection.find_one,
                {DataConstStrings.username_key: validated_user.username}
            )
            if existing_user:
                return Response(
                    status=ResponseStatus.ERROR,
                    data={
                        ZMQConstStrings.error_message: DataErrorsMessagesConstStrings.username_already_exist}
                )
            hashed_password = bcrypt.hashpw(validated_user.password.encode(
                ConstStrings.encode), bcrypt.gensalt())
            validated_user.password = hashed_password.decode(
                ConstStrings.encode)
            user_data_to_insert = validated_user.model_dump(
                by_alias=True, exclude_none=True, exclude_unset=False)
            result = self._handle_db_operation(
                self.collection.insert_one, user_data_to_insert)

            return Response(
                status=ResponseStatus.SUCCESS,
                data={DataConstStrings.inserted_id_key: str(
                    result.inserted_id)}
            )

        except Exception as e:
            return Response(
                status=ResponseStatus.ERROR,
                data={ZMQConstStrings.error_message: str(e)}
            )

    def login(self, login_data: LoginUser) -> Response:
        try:
            user = self._handle_db_operation(
                self.collection.find_one,
                {DataConstStrings.username_key: login_data.get(DataConstStrings.username_key)}
            )
            if not user:
                return Response(
                    status=ResponseStatus.ERROR,
                    data={
                        ZMQConstStrings.error_message: DataErrorsMessagesConstStrings.incorrect_username_or_password}
                )
            if not bcrypt.checkpw(login_data.get(DataConstStrings.password_key).encode(ConstStrings.encode), user[DataConstStrings.password_key].encode(ConstStrings.encode)):
                return Response(
                    status=ResponseStatus.ERROR,
                    data={
                        ZMQConstStrings.error_message: DataErrorsMessagesConstStrings.incorrect_username_or_password}
                )
            return Response(
                status=ResponseStatus.SUCCESS,
                data={
                    DataConstStrings.user_id_key: str(user[DataConstStrings.id_key]),
                    DataConstStrings.username_key: user[DataConstStrings.username_key],
                    "role": user["role"]
                }
            )

        except Exception as e:
            return Response(
                status=ResponseStatus.ERROR,
                data={ZMQConstStrings.error_message: str(e)}
            )
    
    def get_all_users(self) -> Response:
        try:
            print("ctrl db")
            users = list(self._handle_db_operation(self.collection.find, {DataConstStrings.is_active_key: True}))
            # הסרת הסיסמה מהרשומות
            for user in users:
                user.pop(DataConstStrings.password_key, None)
                user[DataConstStrings.id_key] = str(user[DataConstStrings.id_key])
            return Response(
                status=ResponseStatus.SUCCESS,
                data={DataConstStrings.users_key: users}
            )
        except Exception as e:
            return Response(
                status=ResponseStatus.ERROR,
                data={ZMQConstStrings.error_message: str(e)}
            )

    def get_user_by_id(self, user_id: str) -> Response:
        try:
            user = self._handle_db_operation(self.collection.find_one, {DataConstStrings.id_key: ObjectId(user_id)})
            if not user:
                return Response(
                    status=ResponseStatus.ERROR,
                    data={ZMQConstStrings.error_message: DataErrorsMessagesConstStrings.user_not_found}
                )
            user.pop(DataConstStrings.password_key, None)
            user[DataConstStrings.id_key] = str(user[DataConstStrings.id_key])
            return Response(
                status=ResponseStatus.SUCCESS,
                data={DataConstStrings.user_key: user}
            )
        except Exception as e:
            return Response(
                status=ResponseStatus.ERROR,
                data={ZMQConstStrings.error_message: str(e)}
            )

    def get_user_by_username_and_password(self, username: str, password: str) -> Response:
        try:
            user = self._handle_db_operation(self.collection.find_one, {DataConstStrings.username_key: username})
            if not user or not bcrypt.checkpw(password.encode(ConstStrings.encode), user[DataConstStrings.password_key].encode(ConstStrings.encode)):
                return Response(
                    status=ResponseStatus.ERROR,
                    data={ZMQConstStrings.error_message: DataErrorsMessagesConstStrings.incorrect_username_or_password}
                )
            user.pop(DataConstStrings.password_key, None)
            user[DataConstStrings.id_key] = str(user[DataConstStrings.id_key])
            return Response(
                status=ResponseStatus.SUCCESS,
                data={DataConstStrings.user_key: user}
            )
        except Exception as e:
            return Response(
                status=ResponseStatus.ERROR,
                data={ZMQConstStrings.error_message: str(e)}
            )
    
    def delete_user(self, user_id: str) -> None:
        try:
            print("delete user db", user_id)
            result = self._handle_db_operation(
                self.collection.update_one,
                {DataConstStrings.id_key: ObjectId(
                    user_id), DataConstStrings.is_active_key: True},
                {DatabaseConstStrings.set_operator: {
                    DataConstStrings.is_active_key: False}}
            )
            print(result)
            if not result.modified_count or user_id == None:
                return Response(
                    status=ResponseStatus.ERROR,
                    data={
                        ZMQConstStrings.error_message: DataErrorsMessagesConstStrings.user_id_not_found_exception}
                )
            return Response(
                status=ResponseStatus.SUCCESS
            )
        except Exception as e:
            return Response(
                status=ResponseStatus.ERROR,
                data={ZMQConstStrings.error_message: str(e)}
            )

    def update_user(self, user_id: str, user: UserModel) -> None:
        try:
            print("user_id", user_id, user)
            validated_user = UserModel(**user)
            print("validated_user", validated_user)
            user_data_to_update=validated_user.model_dump(
                by_alias=True, exclude_none=True, exclude_unset=False)
            user_data_to_update.pop(DataConstStrings.id_key, None)
            result=self._handle_db_operation(
                self.collection.update_one,
                {DataConstStrings.id_key: ObjectId(
                    user_id), DataConstStrings.is_active_key: True},
                {DatabaseConstStrings.set_operator: user_data_to_update}
            )
            print("result", result)
            if result.modified_count == 0:
                return Response(
                    status=ResponseStatus.ERROR,
                    data={
                        ZMQConstStrings.error_message: DataErrorsMessagesConstStrings.update_user_exception}
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
                DataErrorsMessagesConstStrings.person_duplicate_key_exception)
        except Exception as e:
            raise Exception(
                f"{DataErrorsMessagesConstStrings.general_exception} {e}")

    def _create_jwt_token(self, user: Dict) -> str:
        try:
            exp_delta_seconds = int(os.getenv(ConstStrings.jwt_exp_delta_seconds_env_key))
        except (TypeError, ValueError):
            raise ValueError("Invalid value for JWT expiration delta seconds")
        payload = {
            DataConstStrings.user_id_key: str(user[DataConstStrings.id_key]),
            DataConstStrings.username_key: user[DataConstStrings.username_key],
            DataConstStrings.exp_key: datetime.datetime.now(
            ) + datetime.timedelta(seconds=exp_delta_seconds)
        }
        token = jwt.encode(payload, os.getenv(ConstStrings.jwt_secret_env_key),
                           algorithm=os.getenv(ConstStrings.jwt_algorithm_env_key))
        return token
