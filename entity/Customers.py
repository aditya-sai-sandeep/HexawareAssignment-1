class Customers:
    def __init__(self, customer_id, first_name, last_name, email, phone, address):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.address = address

    def UpdateCustomerInfo(self, new_email, new_phone, new_address):
        self.email = new_email
        self.phone = new_phone
        self.address = new_address

    def CalculateTotalOrders(self):
        pass


    def GetCustomerDetails(self):
        details = (
            f"Customer Details: {self.first_name} {self.last_name}\n"
            f"Email: {self.email}\n"
            f"Phone: {self.phone}\n"
            f"Address: {self.address}"
        )
        return details

customer = Customers(1, "Aditya", "Nagavolu", "aditya@gmail.com", "12345567", "Hills Road")

details = customer.GetCustomerDetails()

customer.UpdateCustomerInfo("adityanew@example.com", "98375235", "Down Hillst")

updated_details = customer.GetCustomerDetails()
