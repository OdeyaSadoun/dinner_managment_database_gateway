import os
import jwt
import bcrypt
import datetime
from typing import Any, Dict
from pymongo.errors import DuplicateKeyError

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
            print("login_data", login_data)
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
            token = self._create_jwt_token(user)
            return Response(
                status=ResponseStatus.SUCCESS,
                data={
                    DataConstStrings.user_id_key: str(user[DataConstStrings.id_key]),
                    DataConstStrings.username_key: user[DataConstStrings.username_key],
                    DataConstStrings.token_key: token
                }
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
