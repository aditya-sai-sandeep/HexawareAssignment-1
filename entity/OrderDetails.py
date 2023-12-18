class OrderDetails:
    def __init__(self, order_detail_id, order, product, quantity):
        self.order_detail_id = order_detail_id
        self.order = order
        self.product = product
        self.quantity = quantity

    def CalculateSubtotal(self):
        pass


    def GetOrderDetailInfo(self):
        info = (
            f"Order Detail ID: {self.order_detail_id}\n"
            f"Product: {self.product.product_name}\n"
            f"Quantity: {self.quantity}\n"
        )
        return info

    def UpdateQuantity(self, new_quantity):
        pass

    def AddDiscount(self, discount_amount):
        pass


# Example usage:
from Orders import Orders
from Products import Products

order = Orders(1, None, None, 0.0)
product = Products(1, "Laptop", "High-performance laptop", 999.99)
order_detail = OrderDetails(1, order, product, 2)

info = order_detail.GetOrderDetailInfo()
