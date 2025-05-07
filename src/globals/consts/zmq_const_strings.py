class ZMQConstStrings: 
    base_tcp_connection_strings = "tcp://"

    # ? Request format identifiers
    resource_identifier = "resource"
    operation_identifier = "operation"
    data_identifier = "data"

    # ? Response format indentifiers
    status_identifier = "status"
    data_identifier = "data"

    # ? Response statuses
    success_status = "success"
    error_status = "error"

    # ? Error messages
    error_message = 'ERROR: '
    unknown_resource_error_message = "Unknown resource"
    unknown_operation_error_message = "Unknown operation"

    # ? Person operations
    get_all_people = "get_all_people"
    get_manual_people = "get_manual_people"
    get_person_by_id = "get_person_by_id"
    create_person = "create_person"
    update_person = "update_person"
    delete_person = "delete_person"
    seat_person = "seat_person"
    unseat_person = "unseat_person"
    import_people_from_csv = "import_people_from_csv"
    
    # ? Table operations
    get_all_tables = "get_all_tables"
    get_table_by_id = "get_table_by_id"
    create_table = "create_table"
    update_table = "update_table"
    update_table_position = "update_table_position"
    delete_table = "delete_table"
    add_person_to_table = "add_person_to_table"
    remove_person_from_table = "remove_person_from_table"
    
    # ? Authorozation operations
    register = "register"
    login = "login"
    get_all_users = "get_all_users"
    get_user_by_id = "get_user_by_id"
    get_user_by_username_and_password = "get_user_by_username_and_password"
    delete_user = "delete_user"
    update_user = "update_user"
    
        # ? Resources
    auth_resource = "auth"
    person_resource = "person"
    table_resource = "table"