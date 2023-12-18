import re

class InvalidEmailError(Exception):
    def __init__(self, email, message="Invalid email format"):
        self.email = email
        self.message = f'{email} should end with @gmail.com or @yahoo.com'
        super().__init__(self.message)




def validate_email(email):
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@(gmail\.com|yahoo\.com)$')
    if not email_pattern.match(email):
        raise InvalidEmailError(email)
