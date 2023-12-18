from exceptions.CustomError import CustomError
from exceptions.InvalidIDError import InvalidIDError
from exceptions.InvalidQuantityError import InvalidQuantityError
from util.DBConnUtil import dbConnection
import decimal

class OrderDetails(dbConnection):

    def create(self):
        create_orderdetails_str = '''
        CREATE TABLE IF NOT EXISTS OrderDetails (
            OrderDetailID INT PRIMARY KEY AUTO_INCREMENT,
            OrderID INT,
            ProductID INT,
            Quantity INT,
            FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON DELETE CASCADE,
            FOREIGN KEY (ProductID) REFERENCES Products(ProductID) ON DELETE CASCADE
        );
        '''
        self.open()
        self.stmt.execute(create_orderdetails_str)
        self.stmt.close()
        print('OrderDetails Tables created successfully------:')

    def addOrderDetail(self):
        OrderID = int(input('Enter Order ID:'))
        if not isinstance(OrderID, int) or OrderID < 0:
            raise InvalidIDError()
        self.OrderID = OrderID

        ProductID = int(input('Enter Product ID:'))
        if not isinstance(ProductID, int):
            raise InvalidIDError()
        self.ProductID = ProductID

        Quantity = int(input('Enter Quantity:'))
        if not isinstance(Quantity, int) or Quantity<0:
            raise InvalidQuantityError()
        self.Quantity = Quantity

        data = [(self.OrderID, self.ProductID, self.Quantity)]
        insert_orderdetail_str = '''INSERT INTO OrderDetails (OrderID, ProductID, Quantity) 
                                    VALUES (%s, %s, %s)'''

        self.open()
        self.stmt.executemany(insert_orderdetail_str, data)
        self.conn.commit()
        print('OrderDetail Record Inserted Successfully..')
        self.close()

    def selectOrderDetails(self):
        self.open()
        select_orderdetails_str = '''SELECT * FROM OrderDetails'''
        self.stmt.execute(select_orderdetails_str)
        records = self.stmt.fetchall()
        print('')
        print('_________________Records In OrderDetails Table________________________')
        for record in records:
            print(record)
        self.close()

    def updateOrderDetail(self):
        self.selectOrderDetails()
        order = int(input('Input OrderDetail ID to be Updated: '))
        if not isinstance(order, int) or order < 0:
            raise InvalidIDError()
        orderDetailId = order
        update_orderdetail_str = 'UPDATE OrderDetails SET '
        data = []

        self.orderID = int(input('Enter Order ID (Press Enter to skip): '))
        if self.orderID:

            update_orderdetail_str += 'OrderID=%s, '
            data.append(self.orderID)

        self.productID = int(input('Enter Product ID (Press Enter to skip): '))
        if self.productID:

            update_orderdetail_str += 'ProductID=%s, '
            data.append(self.productID)

        self.quantity = int(input('Enter Quantity (Press Enter to skip): '))
        if self.quantity:

            update_orderdetail_str += 'Quantity=%s, '
            data.append(self.quantity)

        update_orderdetail_str = update_orderdetail_str.rstrip(', ')

        update_orderdetail_str += ' WHERE OrderDetailID=%s'
        data.append(orderDetailId)

        self.open()
        self.stmt.execute(update_orderdetail_str, data)
        self.conn.commit()
        print('OrderDetail Record updated successfully.')
        self.selectOrderDetails()

    def deleteOrderDetail(self):
        OrderDetail_id = int(input('Input OrderDetail ID to be Deleted: '))
        if not isinstance(OrderDetail_id, int):
            raise InvalidIDError()
        else:
            if OrderDetail_id < 0:
                raise InvalidIDError()
        Id = OrderDetail_id
        delete_orderdetail_str = f'DELETE FROM OrderDetails WHERE OrderDetailID={Id}'
        self.open()
        self.stmt.execute(delete_orderdetail_str)
        self.conn.commit()
        print('OrderDetail Record Deleted Successfully..')

    def GetOrderDetails(self, order_id):
        try:
            if not isinstance(order_id, int) or order_id < 0:
                raise InvalidIDError()

            query = '''
                SELECT *
                FROM OrderDetails
                WHERE OrderDetailID = %s
            '''

            self.open()
            self.stmt.execute(query, (order_id,))
            order_details = self.stmt.fetchall()
            self.close()

            if order_details:
                print('\nOrder Details:')
                for detail in order_details:
                    print(f"OrderDetailID: {detail[0]}")
                    print(f"OrderID: {detail[1]}")
                    print(f"ProductID: {detail[2]}")
                    print(f"Quantity: {detail[3]}")
            else:
                print(f'No order details found for OrderID {order_id}.')

        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

    def CalculateSubtotal(self):
        orderDetailId = int(input('Input OrderDetailID : '))
        if orderDetailId < 0 or orderDetailId < 0:
            raise InvalidIDError()
        self.open()
        statement = '''select  Price,Quantity from OrderDetails
        inner join Products on Products.ProductID = OrderDetails.ProductID
        where OrderDetails.OrderDetailID = %s
        '''
        self.stmt.execute(statement, (orderDetailId,))
        records = self.stmt.fetchone()
        print(float(records[0]) * records[1])
        self.close()

    def AddDiscount(self, dis):
        if not isinstance(dis, (int, float)) or dis < 0 or dis > 100:
            raise CustomError("discount should be between 0-100")
        self.discount = dis

    def SalesReporting(self):
        self.open()
        select_orderdetails_str = '''SELECT ProductID,SUM(Quantity) FROM OrderDetails group by ProductID'''
        self.stmt.execute(select_orderdetails_str)
        records = self.stmt.fetchall()
        print('')
        print('_________________Sales Report________________________')
        for record in records:
            print(f"Product ID is {record[0]} sold {int(record[1])} units")
        self.close()