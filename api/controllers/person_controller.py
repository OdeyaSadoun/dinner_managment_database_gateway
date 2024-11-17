from globals.consts.database_const_strings import DatabaseConstStrings


class PersonController:
    def __init__(self, database_manager):
        self.collection = database_manager.db[DatabaseConstStrings.people_collection]
        self._ensure_indexes_creation()