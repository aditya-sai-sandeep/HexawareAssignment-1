from exceptions.InvalidIDError import InvalidIDError
from exceptions.InvalidPriceError import InvalidPriceError
from exceptions.CustomError import CustomError
from util.DBConnUtil import dbConnection
from datetime import datetime
from decimal import Decimal

class Orders(dbConnection):

    def create(self):
        create_orders_str = '''
        CREATE TABLE IF NOT EXISTS Orders (
            OrderID INT PRIMARY KEY AUTO_INCREMENT,
            CustomerID INT,
            OrderDate DATE,
            TotalAmount DECIMAL(7, 2),
            FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID) ON DELETE CASCADE
        );
        '''
        self.open()
        self.stmt.execute(create_orders_str)
        self.stmt.close()
        print('Orders Tables created successfully------:')
        return f'Created succesfully'

    def addOrder(self):

        CustomerID = int(input('Enter CustomerID:'))
        if not isinstance(CustomerID, int) or CustomerID < 0:
            raise InvalidIDError()
        self.CustomerId = CustomerID

        order_date_input = input('Enter Order Date (YYYY-MM-DD) or leave blank for current date: ')

        TotalAmount = int(input('Enter TotalAmount:'))
        if not isinstance(TotalAmount, (int, float)) or TotalAmount<0:
            raise InvalidPriceError()
        self.TotalAmount = TotalAmount

        if not order_date_input:
            order_date = datetime.now().strftime('%Y-%m-%d')
        else:
            order_date = order_date_input

        data = [(self.CustomerId, order_date, self.TotalAmount)]
        insert_order_str = '''INSERT INTO Orders (CustomerID, OrderDate, TotalAmount) 
                              VALUES (%s, %s, %s)'''

        self.open()
        self.stmt.executemany(insert_order_str, data)
        self.conn.commit()
        print('Order Record Inserted Successfully..')
        self.close()

    def GetOrderDetails(self, order_id):
        try:
            if not isinstance(order_id, int) or order_id < 0:
                raise InvalidIDError()
            query = '''
                SELECT OrderID, CustomerID, OrderDate, TotalAmount, Status
                FROM Orders
                WHERE OrderID = %s
            '''

            self.open()
            self.stmt.execute(query, (order_id,))
            order_details = self.stmt.fetchone()

            if order_details:
                print('\nOrder Details:')
                print(f"OrderID: {order_details[0]}")
                print(f"CustomerID: {order_details[1]}")
                print(f"OrderDate: {order_details[2]}")
                print(f"TotalAmount: {order_details[3]}")
                print(f"Status: {order_details[4]}")
            else:
                print(f'Order with OrderID {order_id} not found.')

        except ValueError as ve:
            print(f"Error: {ve}")

        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

        finally:
            self.close()

    def selectOrders(self):
        self.open()
        select_orders_str = '''SELECT * FROM Orders'''
        self.stmt.execute(select_orders_str)
        records = self.stmt.fetchall()
        print('')
        print('_________________Records In Orders Table________________________')
        for record in records:
            print(record)
        self.close()

    def updateOrder(self):
        self.selectOrders()
        order = int(input('Input Order ID to be Updated: '))
        if not isinstance(order, int) or order < 0:
            raise InvalidIDError()
        orderId = order
        update_order_str = 'UPDATE Orders SET '
        data = []

        self.customerID = int(input('Enter Customer ID (Press Enter to skip): '))
        if self.customerID:
            update_order_str += 'CustomerID=%s, '
            data.append(self.customerID)

        self.orderDate = input('Enter Order Date (YYYY-MM-DD) (Press Enter to skip): ')
        if self.orderDate:
            update_order_str += 'OrderDate=%s, '
            data.append(self.orderDate)

        self.totalAmount = input('Enter Total Amount (Press Enter to skip): ')
        if self.totalAmount:
            update_order_str += 'TotalAmount=%s, '
            data.append(self.totalAmount)

        update_order_str = update_order_str.rstrip(', ')

        update_order_str += ' WHERE OrderID=%s'
        data.append(orderId)

        self.open()
        self.stmt.execute(update_order_str, data)
        self.conn.commit()
        print('Order Record updated successfully.')
        self.selectOrders()

    def deleteOrder(self):
        self.selectOrders()
        Order_id = int(input('Input Order ID to be Deleted: '))
        if not isinstance(Order_id, int) or Order_id < 0:
            raise InvalidIDError()
        Id = Order_id
        delete_order_str = f'DELETE FROM Orders WHERE OrderID={Id}'
        self.open()
        self.stmt.execute(delete_order_str)
        self.conn.commit()
        print('Order Record Deleted Successfully..')
        self.selectOrders()

    def CalculateTotalAmount(self):
        try:
            OrderID = int(input('Enter Order ID:'))
            if not isinstance(OrderID, int) or OrderID < 0:
                raise InvalidIDError()

            self.OrderID = OrderID
            self.open()

            statement = '''
                SELECT Price, Quantity
                FROM OrderDetails
                INNER JOIN Orders ON Orders.OrderID = OrderDetails.OrderID
                INNER JOIN Products ON Products.ProductID = OrderDetails.ProductID
                WHERE Orders.OrderID = %s
            '''

            self.stmt.execute(statement, (OrderID,))
            records = self.stmt.fetchall()

            if not records:
                raise CustomError("No records found for the specified Order ID.")

            total_amount = 0

            for record in records:
                price = float(record[0])
                quantity = int(record[1])
                total_amount += price * quantity

            discount = float(input("Enter discount (in percentage):"))

            if discount < 0 or discount > 100:
                raise CustomError("discount should be between 0-100")

            discount /= 100
            total_amount *= (1 - discount)
            print(total_amount)

            update_statement = 'UPDATE Orders SET TotalAmount=%s WHERE OrderID=%s'
            update_data = (Decimal(total_amount), OrderID)

            self.stmt.execute(update_statement, update_data)
            self.conn.commit()
            self.close()
            print("Total Amount after discount:", total_amount)

        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

    def CancelOrder(self, order_id):
        try:
            if not isinstance(order_id, int) or order_id < 0:
                raise InvalidIDError()

            query = '''
                SELECT OrderDetails.Quantity, Inventory.QuantityInStock, Inventory.ProductID
                FROM Orders
                JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
                JOIN Inventory ON OrderDetails.ProductID = Inventory.ProductID
                WHERE Orders.OrderID = %s
            '''
            self.open()
            self.stmt.execute(query, (order_id,))
            result = self.stmt.fetchall()
            if result:
                print('\nUpdating Inventory.QuantityInStock:')
                for row in result:
                    order_quantity = row[0]
                    inventory_quantity = row[1]
                    product_id = row[2]

                    new_quantity_in_stock = inventory_quantity + order_quantity
                    update_query = 'UPDATE Inventory SET QuantityInStock = %s WHERE ProductID = %s'
                    update_data = (new_quantity_in_stock, product_id)
                    self.stmt.execute(update_query, update_data)

                delete_order_str = f'DELETE FROM Orders WHERE OrderID={order_id}'
                self.stmt.execute(delete_order_str)
                self.conn.commit()
                self.close()
                print(f'Order with OrderID {order_id} canceled successfully.')

            else:
                print(f'No data found for OrderID {order_id}.')

        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

    def AlterTable(self):
        alter_str = '''
                ALTER TABLE Orders
                    ADD COLUMN Status VARCHAR(50) DEFAULT 'Processing'
            '''
        self.open()
        self.stmt.execute(alter_str)
        self.conn.commit()
        print('Orders Table altered successfully------:')
        self.close()

    def UpdateOrderStatus(self, order_id, new_status):
        if not isinstance(order_id, int) or order_id < 0:
            raise InvalidIDError()
        if not isinstance(new_status, str):
            raise CustomError("status should be string")
        self.selectOrders()
        update_str = 'UPDATE Orders SET Status = %s WHERE OrderID = %s'
        data = (new_status, order_id)
        self.open()
        self.stmt.execute(update_str, data)
        self.conn.commit()
        print('Order status updated successfully.')
        self.selectOrders()
        self.close()
