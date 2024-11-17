from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os

from globals.consts.consts import Consts
from globals.consts.database_const_strings import DatabaseConstStrings
from globals.consts.data_errors_messages_const_strings import DataErrorsMessagesConstStrings
from infrastructures.interfaces.idatabase_manager import IDatabaseManager


class MongoDBDatabaseManager(IDatabaseManager):
    def __init__(self):
        self._db = None
        self.connect()

    def connect(self):
        mongo_uri = os.getenv(DatabaseConstStrings.mongo_uri, DatabaseConstStrings.connection_string)    
        database_name = os.getenv(DatabaseConstStrings.database_name, DatabaseConstStrings.default_database_name)
        
        try:
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=Consts.server_selection_timeout_ms) 
            self._db = client[database_name]
            self.test_connection()
        except ConnectionFailure as e:
            raise ConnectionFailure(f"{DataErrorsMessagesConstStrings.connection_exception} {e}")

    def test_connection(self):
        try:
            self._db.command(DatabaseConstStrings.ping)
        except ConnectionFailure as e:
            raise ConnectionFailure("{DataErrorsMessagesConstStrings.connection_exception} {e}")

    @property
    def db(self):
        if self._db is None:
            raise ConnectionFailure(DataErrorsMessagesConstStrings.connetion_not_established_exception)
        return self._db