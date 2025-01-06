class DatabaseConstStrings:
    ping = "ping"

    # ? Mongo connection
    mongo_uri = "MONGO_URI"
    connection_string = "mongodb://localhost:27017"
    database_name = "DATABASE_NAME"
    default_database_name = "default_db"

    people_collection = "people"
    tables_collection = "tables"
    users_collection = "users"
    
    # ? operators
    or_operator = "$or"
    gte_operator = "$gte"
    lte_operator = "$lte"
    set_operator = "$set"
    push_operator = "$push"
    pull_operator = "$pull"

    # ? indexes
    index_name = "name"
    unique_index = "unique"