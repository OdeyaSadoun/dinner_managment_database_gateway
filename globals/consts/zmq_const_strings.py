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

    # ? Guard operations
    get_guard_by_id = "get_guard_by_id"
    get_guards_by_person_id = "get_guards_by_person_id"
    get_all_guards = "get_all_guards"
    get_guards_between_dates = "get_guards_between_dates"
    create_guards = "create_guards"
    update_guard = "update_guard"

    # ? Person operations
    get_all_people = "get_all_people"
    get_person_by_id = "get_person_by_id"
    get_person_by_personal_number = "get_person_by_personal_number"
    create_person = "create_person"
    update_person = "update_person"
    delete_person = "delete_person"