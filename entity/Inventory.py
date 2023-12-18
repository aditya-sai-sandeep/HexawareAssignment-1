from datetime import datetime
from Products import Products
class Inventory:
    def __init__(self, inventoryID, product, quantityInStock, lastStockUpdate):
        self.inventoryID = inventoryID
        self.product = product
        self.quantityInStock = quantityInStock
        self.lastStockUpdate = lastStockUpdate

    def GetProduct(self):
        return self.product

    def GetQuantityInStock(self):
        return self.quantityInStock

    def AddToInventory(self, quantity):
        pass

    def RemoveFromInventory(self, quantity):
        pass

    def UpdateStockQuantity(self, newQuantity):
        pass

    def IsProductAvailable(self, quantityToCheck):
        pass

    def GetInventoryValue(self):
        pass

    def ListLowStockProducts(self, threshold):
        pass

    def ListOutOfStockProducts(self):
        pass

product = Products(1, "Laptop", "High-performance laptop", 999.99)
inventory = Inventory(1, product, 5, datetime.now())
