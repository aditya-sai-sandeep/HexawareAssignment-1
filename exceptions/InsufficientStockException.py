class InsufficientStockException(Exception):
    def __init__(self, message="Requested stock is more than available"):
        self.message = message
        super().__init__(self.message)
