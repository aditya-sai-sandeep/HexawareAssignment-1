from datetime import datetime
from Customers import Customers


class Orders:
    def __init__(self, order_id, customer, order_date, total_amount):
        self.order_id = order_id
        self.customer = customer
        self.order_date = order_date
        self.total_amount = total_amount

    def CalculateTotalAmount(self):
        pass

    def GetOrderDetails(self):
        details = (
            f"Order ID: {self.order_id}\n"
            f"Order Date: {self.order_date}\n"
            f"Total Amount: ${self.total_amount}\n"
            f"Customer Details:\n{self.customer.GetCustomerDetails()}"
        )
        return details

    def UpdateOrderStatus(self, new_status):
        pass

    def CancelOrder(self):
        pass


customer = Customers(1, "Aditya", "Nagavolu", "aditya@gmail.com", "12345567", "Hills Road")

order_date = datetime.now()
order = Orders(1, customer, order_date, 0.0)

details = order.GetOrderDetails()

order.UpdateOrderStatus("Shipped")
