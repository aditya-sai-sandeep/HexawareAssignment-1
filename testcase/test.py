import unittest

from dao.Customers import Customers
from dao.Orders import Orders
from dao.Products import Products


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.customers1 = Customers()
        self.products1 = Products()
        self.orders1 = Orders()
    def test1(self):
        result = self.customers1.select()
        self.assertEqual('Customers details fetched successfully', str(result))

    def test2(self):
        result = self.products1.selectProducts()
        self.assertEqual('Products details fetched successfully', str(result))
    def test3(self):
        result = self.orders1.create()
        self.assertEqual('Created succesfully', str(result))

if __name__ == '__main__':
    unittest.main()
