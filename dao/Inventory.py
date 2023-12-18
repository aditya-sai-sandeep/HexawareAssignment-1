from exceptions.InvalidIDError import InvalidIDError
from exceptions.InvalidQuantityError import InvalidQuantityError
from util.DBConnUtil import dbConnection
from exceptions.InsufficientStockException import InsufficientStockException
from datetime import datetime


class Inventory(dbConnection):

    def create(self):
        create_inventory_str = '''
        CREATE TABLE IF NOT EXISTS Inventory (
            InventoryID INT PRIMARY KEY AUTO_INCREMENT,
            ProductID INT,
            QuantityInStock INT,
            LastStockUpdate TIMESTAMP,
            FOREIGN KEY (ProductID) REFERENCES Products(ProductID) ON DELETE CASCADE
        );
        '''
        self.open()
        self.stmt.execute(create_inventory_str)
        self.stmt.close()
        print('Inventory Tables created successfully------:')

    def addInventory(self):
        ProductID = int(input('Enter Product ID:'))
        if not isinstance(ProductID, int) or ProductID < 0:
            raise InvalidIDError()
        self.productID = ProductID

        QuantityInStock = int(input('Enter Quantity in stock:'))
        if not isinstance(QuantityInStock, int)or QuantityInStock<0:
            raise InvalidQuantityError()
        self.quantityInStock = QuantityInStock
        last_Stock_Update = input("enter date:")
        if not last_Stock_Update:
            self.lastStockUpdate = datetime.now().strftime('%Y-%m-%d')
        self.lastStockUpdate = last_Stock_Update
        data = [(self.productID, self.quantityInStock, self.lastStockUpdate)]
        insert_inventory_str = '''INSERT INTO Inventory (ProductID, QuantityInStock, LastStockUpdate) 
                                  VALUES (%s, %s, %s)'''

        self.open()
        self.stmt.executemany(insert_inventory_str, data)
        self.conn.commit()
        print('Inventory Record Inserted Successfully..')
        self.close()
    def selectInventory(self):
        self.open()
        select_inventory_str = '''SELECT * FROM Inventory'''
        self.stmt.execute(select_inventory_str)
        records = self.stmt.fetchall()
        print('')
        print('_________________Records In Inventory Table________________________')
        for record in records:
            print(record)
        self.close()

    def updateInventory(self):
        self.selectInventory()
        Inventory_id = int(input('Input Inventory ID to be Deleted: '))
        if not isinstance(Inventory_id, int) or Inventory_id < 0:
            raise InvalidIDError()
        inventoryId = Inventory_id
        update_inventory_str = 'UPDATE Inventory SET '
        data = []

        self.productID = int(input('Enter Product ID (Press Enter to skip): '))
        if self.productID:
            update_inventory_str += 'ProductID=%s, '
            data.append(self.productID)

        self.quantityInStock = int(input('Enter Quantity in Stock (Press Enter to skip): '))
        if self.quantityInStock:
            update_inventory_str += 'QuantityInStock=%s, '
            data.append(self.quantityInStock)

        self.lastStockUpdate = input('Enter Last Stock Update (YYYY-MM-DD HH:MM:SS) (Press Enter to skip): ')
        if self.lastStockUpdate:
            update_inventory_str += 'LastStockUpdate=%s, '
            data.append(self.lastStockUpdate)

        update_inventory_str = update_inventory_str.rstrip(', ')

        update_inventory_str += ' WHERE InventoryID=%s'
        data.append(inventoryId)

        self.open()
        self.stmt.execute(update_inventory_str, data)
        self.conn.commit()
        print('Inventory Record updated successfully.')
        self.selectInventory()

    def deleteInventory(self):
        Inventory_id = int(input('Input Inventory ID to be Deleted: '))
        if not isinstance(Inventory_id, int):
            raise InvalidIDError()
        else:
            if Inventory_id < 0:
                raise InvalidIDError()
        inventoryId = Inventory_id
        delete_inventory_str = f'DELETE FROM Inventory WHERE InventoryID={inventoryId}'
        self.open()
        self.stmt.execute(delete_inventory_str)
        self.conn.commit()
        print('Inventory Record Deleted Successfully..')

    def GetProduct(self):
        try:
            product_id = int(input('Enter Product ID to get product details: '))
            if not isinstance(product_id, int) or product_id < 0:
                raise InvalidIDError()

            self.open()
            query = '''
                SELECT Products.*
                FROM Products
                INNER JOIN Inventory ON Products.ProductID = Inventory.ProductID
                WHERE Inventory.ProductID = %s
            '''

            self.stmt.execute(query, (product_id,))
            product_data = self.stmt.fetchone()

            if product_data:
                print('\nProduct Details:')
                print(f"ProductID: {product_data[0]}")
                print(f"ProductName: {product_data[1]}")
                print(f"Description: {product_data[2]}")
                print(f"Price: {product_data[3]}")
            else:
                print(f'No product found with ProductID: {product_id}')
            self.close()
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

    def GetQuantityInStock(self):
        try:
            inventory_id = int(input("enter inventiry number:"))
            if not isinstance(inventory_id, int) or inventory_id < 0:
                raise InvalidIDError()

            self.open()
            query = '''
                SELECT QuantityInStock
                FROM Inventory
                WHERE InventoryID = %s
            '''

            self.stmt.execute(query, (inventory_id,))
            quantity_in_stock = self.stmt.fetchone()

            if quantity_in_stock:
                print(f'Quantity in Stock for InventoryID {inventory_id}: {quantity_in_stock[0]}')
            else:
                print(f'No data found for InventoryID: {inventory_id}')
            self.close()
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

    def AddToInventory(self):
        try:
            inventory_id = int(input("enter inventory Id"))
            if not isinstance(inventory_id, int) or inventory_id < 0:
                raise InvalidIDError()
            quantity = int(input("enter quantity"))
            if not isinstance(quantity, int) or quantity <= 0:
                raise InvalidQuantityError()

            self.open()
            get_inventory_query = '''
                SELECT ProductID, QuantityInStock
                FROM Inventory
                WHERE InventoryID = %s
            '''
            self.stmt.execute(get_inventory_query, (inventory_id,))
            inventory_data = self.stmt.fetchone()

            if not inventory_data:
                print(f'No data found for InventoryID: {inventory_id}')
                return

            product_id, current_quantity = inventory_data

            new_quantity = current_quantity + quantity

            update_inventory_query = '''
                UPDATE Inventory
                SET QuantityInStock = %s
                WHERE InventoryID = %s
            '''

            self.stmt.execute(update_inventory_query, (new_quantity, inventory_id))
            self.conn.commit()
            self.close()
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

    def RemoveFromInventory(self):
        try:
            inventory_id = int(input("enter inventory Id"))
            if not isinstance(inventory_id, int) or inventory_id < 0:
                raise InsufficientStockException()
            quantity = int(input("enter quantity"))
            if not isinstance(quantity, int) or quantity <= 0:
                raise InvalidQuantityError()

            self.open()
            get_inventory_query = '''
                SELECT ProductID, QuantityInStock
                FROM Inventory
                WHERE InventoryID = %s
            '''
            self.stmt.execute(get_inventory_query, (inventory_id,))
            inventory_data = self.stmt.fetchone()

            if not inventory_data:
                print(f'No data found for InventoryID: {inventory_id}')
                return

            product_id, current_quantity = inventory_data

            new_quantity = current_quantity - quantity
            if new_quantity < 0:
                raise InvalidQuantityError("quantity cant be -ve")

            update_inventory_query = '''
                UPDATE Inventory
                SET QuantityInStock = %s
                WHERE InventoryID = %s
            '''

            self.stmt.execute(update_inventory_query, (new_quantity, inventory_id))
            self.conn.commit()
            self.close()
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

    def UpdateStockInventory(self):
        try:
            inventory_id = int(input("enter inventory Id"))
            if not isinstance(inventory_id, int) or inventory_id < 0:
                raise InvalidIDError()
            quantity = int(input("enter quantity"))
            if not isinstance(quantity, int) or quantity <= 0:
                raise InvalidQuantityError()

            self.open()
            get_inventory_query = '''
                SELECT ProductID, QuantityInStock
                FROM Inventory
                WHERE InventoryID = %s
            '''
            self.stmt.execute(get_inventory_query, (inventory_id,))
            inventory_data = self.stmt.fetchone()

            if not inventory_data:
                print(f'No data found for InventoryID: {inventory_id}')
                return

            product_id, current_quantity = inventory_data

            new_quantity = quantity
            update_inventory_query = '''
                UPDATE Inventory
                SET QuantityInStock = %s
                WHERE InventoryID = %s
            '''

            self.stmt.execute(update_inventory_query, (new_quantity, inventory_id))
            self.conn.commit()
            self.close()
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

    def IsProductAvailable(self):
        try:
            inventory_id = int(input("enter inventory Id"))
            if not isinstance(inventory_id, int) or inventory_id < 0:
                raise InvalidIDError()
            quantity_to_check = int(input("enter quantity"))
            if not isinstance(quantity_to_check, int) or quantity_to_check <= 0:
                raise InvalidQuantityError()

            self.open()
            get_inventory_query = '''
                SELECT QuantityInStock
                FROM Inventory
                WHERE InventoryID = %s
            '''
            self.stmt.execute(get_inventory_query, (inventory_id,))
            current_quantity = self.stmt.fetchone()

            if not current_quantity:
                print(f'No data found for InventoryID: {inventory_id}')
                return False

            current_quantity = current_quantity[0]

            if current_quantity >= quantity_to_check:
                return True
            else:
                self.close()
                return False
        except Exception as e:
            print(e)
            return False

    def GetInventoryValue(self):
        try:
            self.open()
            get_inventory_value_query = '''
                SELECT SUM(Products.Price * Inventory.QuantityInStock) AS TotalValue
                FROM Inventory
                INNER JOIN Products ON Inventory.ProductID = Products.ProductID
            '''
            self.stmt.execute(get_inventory_value_query)
            records = self.stmt.fetchall()
            for i in records:
                print(i[0])
            else:
                print("data is not there")
            self.close()
        except Exception as e:
            print(e)

    def ListLowStockProducts(self):
        try:
            threshold = int(input("enter threshold"))
            if not isinstance(threshold, int) or threshold < 0:
                raise InvalidIDError()
            self.open()
            statement = 'SELECT InventoryID, ProductID FROM Inventory WHERE QuantityInStock < %s'
            self.stmt.execute(statement, (threshold,))
            result = self.stmt.fetchall()
            if result:
                for i in result:
                    print(i)
            else:
                print("all are more ")
            self.close()
        except Exception as e:
            print(e)

    def ListOutOfStockProducts(self):
        try:
            self.open()
            statement = 'SELECT InventoryID, ProductID FROM Inventory WHERE QuantityInStock =0'
            self.stmt.execute(statement)
            result = self.stmt.fetchall()
            if result:
                for i in result:
                    print(i)
            else:
                print("all are available")

            self.close()
        except Exception as e:
            print(e)
