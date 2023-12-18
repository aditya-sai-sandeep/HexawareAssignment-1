from exceptions.InvalidDataException import InvalidEmailError , validate_email
from exceptions.InvalidIDError import InvalidIDError
from exceptions.InvalidNameError import InvalidNameError , StringCheck
from exceptions.InvalidPhoneError import InvalidPhoneError , validate_phone
from util.DBConnUtil import dbConnection


class Customers(dbConnection):

    def __init__(self):
        self.name = ''
        self.email = ''
        self.phone = ''
        print(self.name, self.email, self.name)

    def create(self):
        create_str = '''
        CREATE TABLE IF NOT EXISTS Customers (
        CustomerID INT PRIMARY KEY AUTO_INCREMENT,
        FirstName VARCHAR(55),
        LastName VARCHAR(55),
        Email VARCHAR(55),
        Phone VARCHAR(20),
        Address VARCHAR(55)
                );
        '''
        self.open()
        self.stmt.execute(create_str)
        self.stmt.close()
        print('Customers Table created successfully------:')

    def addCustomer(self):

        first_name = input('Enter First Name :')
        if not isinstance(first_name, str):
            raise InvalidNameError()
        StringCheck(first_name)
        self.firstname = first_name

        last_name = input('Enter Last Name :')
        if not isinstance(last_name, str):
            raise InvalidNameError()
        StringCheck(last_name)
        self.lastname = last_name

        Email = input('Enter email:')
        if not isinstance(Email, str):
            raise InvalidEmailError()
        validate_email(Email)
        self.email = Email

        Phone = input('Enter phone :')
        if not isinstance(Phone, str):
            raise InvalidPhoneError()
        validate_phone(Phone)
        self.phone = Phone

        Address = input('Enter address :')
        self.address = Address

        data = [(self.firstname, self.lastname, self.email, self.phone, self.address)]
        insert_str = '''insert into Customers(FirstName,LastName,Email,Phone,Address) 
        values(%s,%s,%s,%s,%s)'''
        self.open()
        self.stmt.executemany(insert_str, data)
        self.conn.commit()
        print('Records Inserted Successfully..')
        self.close()

    def select(self):
        self.open()
        select_str = '''select * from customers'''
        self.stmt.execute(select_str)
        recods = self.stmt.fetchall()
        print('')
        print('_________________Records In Customer Table________________________')
        for i in recods:
            print(i)
        self.close()

    def UpdateCustomerInfo(self):
        self.select()
        customer_id = int(input('Input Customer ID to be Updated: '))
        if not isinstance(customer_id, int):
            raise InvalidIDError()
        else:
            if customer_id < 0:
                raise InvalidIDError()
        Id = customer_id
        update_str = 'UPDATE customers SET '
        data = []

        first_name = input('Enter First Name ((Press Enter to skip)):')
        if first_name:
            if not isinstance(first_name, str):
                raise InvalidNameError()
            StringCheck(first_name)
            self.firstname = first_name
            update_str += 'FirstName=%s, '
            data.append(self.firstname)

        last_name = input('Enter Last Name ((Press Enter to skip)):')
        if last_name:
            if not isinstance(last_name, str):
                raise InvalidNameError()
            StringCheck(last_name)
            self.lastname = last_name
            update_str += 'LastName=%s, '
            data.append(self.lastname)

        Email = input('Enter email:(Press Enter to skip)')
        if Email:
            if not isinstance(Email, str):
                raise InvalidEmailError()
            validate_email(Email)
            self.email = Email
            update_str += 'Email=%s, '
            data.append(self.email)

        Phone = input('Enter Phone (Press Enter to skip): ')
        if Phone:
            if not isinstance(Phone, str):
                raise InvalidPhoneError()
            validate_phone(Phone)
            self.phone = Phone
            update_str += 'Phone=%s, '
            data.append(self.phone)

        update_str = update_str.rstrip(', ')

        update_str += ' WHERE CustomerID=%s'
        data.append(Id)

        self.open()
        self.stmt.execute(update_str, data)
        self.conn.commit()
        print('Record updated successfully.')
        self.select()

    def delete(self):
        customer_id = int(input('Input Customer ID to be Updated: '))
        if not isinstance(customer_id, int) or customer_id < 0:
            raise InvalidIDError()
        Id = customer_id
        delete_str = f'delete from customers where CustomerID={Id}'
        # data=[(Id,)]
        self.open()
        # self.stmt.executemany(delete_str,data)
        self.stmt.execute(delete_str)
        self.conn.commit()
        print('Records Deleted Successfully..')

    def GetCustomerDetails(self, customer_id):
        try:
            if not isinstance(customer_id, int) or customer_id < 0:
                raise InvalidIDError()
            self.open()
            select_customer_str = '''
                SELECT * FROM Customers
                WHERE CustomerID = %s
            '''
            self.stmt.execute(select_customer_str, (customer_id,))
            customer_data = self.stmt.fetchone()

            if not customer_data:
                print(f"No customer found with CustomerID: {customer_id}")
            else:
                print('\nCustomer Details:')
                print(f"CustomerID: {customer_data[0]}")
                print(f"FirstName: {customer_data[1]}")
                print(f"LastName: {customer_data[2]}")
                print(f"Email: {customer_data[3]}")
                print(f"Phone: {customer_data[4]}")
                print(f"Address: {customer_data[5]}")
            self.close()
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

    def CalculateTotalOrders(self, customer_id):
        try:
            # Validate customer_id
            if not isinstance(customer_id, int) or customer_id < 0:
                raise InvalidIDError()

            self.open()
            total_orders_str = '''
                SELECT COUNT(*) FROM Orders
                INNER JOIN Customers ON Orders.CustomerID = Customers.CustomerID
                WHERE Customers.CustomerID = %s
            '''
            self.stmt.execute(total_orders_str, (customer_id,))
            total_orders = self.stmt.fetchone()[0]

            print(f"Total orders placed by CustomerID {customer_id}: {total_orders}")
            self.close()
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")



