from exceptions.InvalidIDError import InvalidIDError
from exceptions.InvalidNameError import InvalidNameError , StringCheck
from exceptions.InvalidPriceError import InvalidPriceError

from util.DBConnUtil import dbConnection


class Products(dbConnection):

    def create(self):
        create_str = '''
        CREATE TABLE IF NOT EXISTS Products (
            ProductID INT PRIMARY KEY AUTO_INCREMENT,
            ProductName VARCHAR(55),
            Description VARCHAR(55),
            Price INT
        );
        '''
        self.open()
        self.stmt.execute(create_str)
        self.stmt.close()
        print('Products Table created successfully------:')

    def addProduct(self):
        Product_Name = input('Enter Product Name :')
        if not isinstance(Product_Name, str):
            raise InvalidNameError()
        StringCheck(Product_Name)
        self.ProductName = Product_Name

        Description = input('Enter Description:')
        self.Description = Description

        new = int(input('Enter Price:'))
        if not isinstance(new, int) or new<0:
            raise InvalidPriceError()
        self.price = new

        data = [(self.ProductName, self.Description, self.price)]
        insert_str = '''INSERT INTO Products (ProductName, Description, Price) 
                        VALUES (%s, %s, %s)'''

        self.open()
        self.stmt.executemany(insert_str, data)
        self.conn.commit()
        print('Records Inserted Successfully..')
        self.close()

    def selectProducts(self):
        self.open()

        select_str = '''SELECT * FROM Products'''
        self.stmt.execute(select_str)
        records = self.stmt.fetchall()
        print('')
        print('_________________Records In Products Table________________________')
        for record in records:
            print(record)
        self.close()
        return f'Products details fetched successfully'

    def UpdateProductInfo(self):
        self.selectProducts()
        Product_id = int(input('Input Product ID to be Updated: '))
        if not isinstance(Product_id, int) or Product_id<0:
            raise InvalidIDError()
        Id = Product_id
        update_str = 'UPDATE Products SET '
        data = []

        Product_name = input('Enter Product Name ((Press Enter to skip)):')
        if Product_name:
            if not isinstance(Product_name, str):
                raise InvalidNameError()
            StringCheck(Product_name)
            self.ProductName = Product_name
            update_str += 'ProductName=%s, '
            data.append(self.ProductName)

        Description = input('Enter Description:(Press Enter to skip)')
        if Description:
            self.Description = Description
            update_str += 'Description=%s, '
            data.append(self.Description)

        Price = input('Enter Price: (Press Enter to skip): ')
        if Price:
            Price = int(Price)
            if not isinstance(Price, (int, float)) or Price < 0:
                raise InvalidPriceError()
            self.Price = int(Price)
            update_str += 'Price=%s, '
            data.append(self.Price)

        update_str = update_str.rstrip(', ')

        update_str += ' WHERE ProductID=%s'
        data.append(Id)

        self.open()
        self.stmt.execute(update_str, data)
        self.conn.commit()
        print('Record updated successfully.')
        self.selectProducts()

    def deleteProduct(self):
        self.selectProducts()
        Product_id = int(input('Input Product ID to be Deleted: '))
        if not isinstance(Product_id, int):
            raise InvalidIDError()
        else:
            if Product_id < 0:
                raise InvalidIDError()
        Id = Product_id
        delete_str = f'DELETE FROM Products WHERE ProductID={Id}'
        self.open()
        self.stmt.execute(delete_str)
        self.conn.commit()
        self.close()
        print('Record Deleted Successfully..')

    def GetProductDetails(self, product_id):
        try:
            # Validate product_id
            if not isinstance(product_id, int) or product_id < 0:
                raise InvalidIDError()

            self.open()
            get_product_details_str = '''
                SELECT * FROM Products
                WHERE ProductID = %s
            '''
            self.stmt.execute(get_product_details_str, (product_id,))
            product_data = self.stmt.fetchone()

            if not product_data:
                print(f"No product found with ProductID: {product_id}")
            else:
                print('\nProduct Details:')
                print(f"ProductID: {product_data[0]}")
                print(f"ProductName: {product_data[1]}")
                print(f"Description: {product_data[2]}")
                print(f"Price: {product_data[3]}")
            self.close()
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

    def IsProductInStock(self, product_id):
        try:
            if not isinstance(product_id, int) or product_id < 0:
                raise InvalidIDError()

            self.open()
            query = '''
                SELECT Inventory.QuantityInStock
                FROM Products
                INNER JOIN Inventory ON Products.ProductID = Inventory.ProductID
                WHERE Products.ProductID = %s
            '''

            self.stmt.execute(query, (product_id,))
            result = self.stmt.fetchone()

            if result and result[0] > 0:
                return True
            else:
                return False

        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            return False
