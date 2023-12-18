class InvalidNameError(Exception):
    def __init__(self, message="Name must be a string and should not contains numbers"):
        self.message = message
        super().__init__(self.message)



def StringCheck(var):
    for i in var:
        if i.isalpha() or i.isspace():
            pass
        else:
            raise InvalidNameError()
