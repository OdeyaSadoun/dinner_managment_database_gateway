from typing import Optional
from globals.consts.data_errors_messages_const_strings import DataErrorsMessagesConstStrings

class PersonValidators:
    @staticmethod
    def validate_phone(value: Optional[str]) -> Optional[str]:
        if value is None or str(value).strip() == "":
            return None  # ריק או None נחשב כאילו לא הוזן
        value = str(value)
        if not value.isdigit():
            raise ValueError(DataErrorsMessagesConstStrings.validate_phone_is_digits_exception)
        if len(value) != 10:
            raise ValueError(DataErrorsMessagesConstStrings.validate_phone_long_exception)
        return value
