class InvalidPhoneError(Exception):
    def __init__(self, message="Phone must be a numbers only"):
        self.message = message
        super().__init__(self.message)


def validate_phone(Phone):
    for i in Phone:
        if i.isdigit():
            pass
        else:
            raise InvalidPhoneError()
