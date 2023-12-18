class InvalidPriceError(Exception):
    def __init__(self, message="Price must be number and positive"):
        self.message = message
        super().__init__(self.message)
