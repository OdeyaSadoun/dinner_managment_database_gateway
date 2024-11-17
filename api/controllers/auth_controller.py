from globals.consts.database_const_strings import DatabaseConstStrings


class AuthController:
    def __init__(self, database_manager):
        self.collection = database_manager.db[DatabaseConstStrings.auth_collection]
        self._ensure_indexes_creation()