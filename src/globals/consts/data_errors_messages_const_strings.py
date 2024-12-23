class DataErrorsMessagesConstStrings:
    error_data_key = "error_data"
    general_exception = "An error occurred:"

    # ? database exception
    connection_exception = "Connection to MongoDB failed:"
    connetion_not_established_exception = "Database connection is not established."

    # ? table exception
    table_duplicate_key_exception = "A table with this id already exists."
    table_id_not_found_exception = "Active table with the given ID not found."
    update_table_exception = "Active table not found or no changes made."

    # ? person exception
    person_duplicate_key_exception = "A person with this id already exists."
    person_id_not_found_exception = "Active person with the given ID not found."
    personal_number_not_found_exception = "Active person with personal number not found."
    update_person_exception = "Active person not found or no changes made."
    invalid_object_id_format_exception = "Invalid ObjectId format: "
    object_id_wrong_type_exception = "Value must be an ObjectId, got "
    
    # ? person validators exception
    validate_personal_number_is_digits_exception = "Personal number must contain only digits."
    validate_personal_number_long_exception = "Personal number must be exactly 8 digits long."
    validate_phone_is_digits_exception = "Phone number must contain only digits."
    validate_phone_long_exception = "Phone number must be exactly 10 digits long."
    validate_birthday_not_past_exception = "Birthday cannot be a future date."
    validate_military_discharge_date_not_past_exception = "Military discharge date cannot be in the past."
    validate_start_date_biger_then_end_date_exception = "Start date of an unavailable date range cannot be after the end date."
    validate_start_date_smaller_then_now_exception = "Unavailable date range cannot start in the past."
    validate_role_invalid_role_exception = "Invalid role: "
    validate_rank_invalid_rank_exception = "Invalid rank: "
    validate_must_be_exception = "Must be one of"
    validate_guards_frequency_invalid_guard_exception = "Invalid guards frequency: "
    validate_check_dates_consistency = "Military discharge date must be after the birthday."
    
    # ? authorization
    username_already_exist = "ERROR: username already exist"
    incorrect_username_or_password = "ERROR: incorrect username or password"