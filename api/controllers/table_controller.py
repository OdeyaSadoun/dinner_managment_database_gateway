from globals.consts.database_const_strings import DatabaseConstStrings


class TableController:
    def __init__(self, database_manager):
        self.collection = database_manager.db[DatabaseConstStrings.tables_collection]
        self._ensure_indexes_creation()