from globals.consts.data_errors_messages_const_strings import DataErrorsMessagesConstStrings


class PersonValidators:
    @staticmethod
    def validate_phone(value: str) -> str:
        """Validate that the phone number contains only digits and is exactly 10 digits long."""
        if not value.isdigit():
            raise ValueError(DataErrorsMessagesConstStrings.validate_phone_is_digits_exception)
        if len(value) != 10: 
            raise ValueError(DataErrorsMessagesConstStrings.validate_phone_long_exception)
        return value