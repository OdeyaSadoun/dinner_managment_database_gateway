class DatabaseConstStrings:
    ping = "ping"

    # ? Mongo connection
    mongo_uri = "MONGO_URI"
    connection_string = "mongodb://localhost:27017"
    database_name = "DATABASE_NAME"
    default_database_name = "default_db"

    guards_collection = "guards"
    people_collection = "people"

    # ? operators
    or_operator = "$or"
    gte_operator = "$gte"
    lte_operator = "$lte"
    set_operator = "$set"

    # ? indexes
    index_name = "name"
    commander_id_index = "commander_id_1"
    deputy_id_index = "deputy_id_1"
    date_index = "date_1"
    personal_number_index = "personal_number_1"
    unique_index = "unique"