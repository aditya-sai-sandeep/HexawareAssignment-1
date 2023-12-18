import mysql.connector as connection

from util.PropertyUtil import PropertyUtil

class dbConnection():
    def _init_(self):
        pass

    def open(self):
        try:
            l = PropertyUtil.getPropertyString()
            self.conn = connection.connect(host=l[0], database=l[3], username=l[1], password=l[2])
            if self.conn:
                print("--Database Is Connected--")
            self.stmt = self.conn.cursor()
        except Exception as e:
            print(e)

    def close(self):
        try:
            self.conn.close()
            print('Connection Closed.')
        except Exception as e:
            print(e)

d = dbConnection()
d.open()
d.close()
