class InvalidIDError(Exception):
    def __init__(self, message="ID must be an integer and must be positive"):
        self.message = message
        super().__init__(self.message)
