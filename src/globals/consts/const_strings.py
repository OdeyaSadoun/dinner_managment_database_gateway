class ConstStrings:
    date_format = "%Y-%m-%d"
    date_time_splitter = "T"
    before_mode_validator = "before"
    encode = "utf-8"

    id_before_serialization = "_id"
    id_after_serialization = "id"
    
    # ? ENV keys
    jwt_secret_env_key = "JWT_SECRET"
    jwt_algorithm_env_key = "JWT_ALGORITHM"
    jwt_exp_delta_seconds_env_key = "JWT_EXP_DELTA_SECONDS"
    localhost_env_key = "LOCAL_HOST"
    port_env_key = "PORT"
