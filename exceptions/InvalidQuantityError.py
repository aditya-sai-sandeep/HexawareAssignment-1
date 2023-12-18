class InvalidQuantityError(Exception):
    def __init__(self, message="Quantity ID must be an integer"):
        self.message = message
        super().__init__(self.message)
