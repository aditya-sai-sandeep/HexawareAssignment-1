class Products:
    def __init__(self, product_id, product_name, description, price):
        self.product_id = product_id
        self.product_name = product_name
        self.description = description
        self.price = price

    def UpdateProductInfo(self, new_description, new_price):
        self.description = new_description
        self.price = new_price

    def IsProductInStock(self):
        pass

    def GetProductDetails(self):
        details = (
            f"Product Details: {self.product_name}\n"
            f"Product ID: {self.product_id}\n"
            f"Description: {self.description}\n"
            f"Price: ${self.price}"
        )
        return details


product = Products(1, "Laptop", "High-performance laptop", 45000)
details = product.GetProductDetails()

product.UpdateProductInfo("Powerful laptop with upgraded features", 50000)
updated_details = product.GetProductDetails()

