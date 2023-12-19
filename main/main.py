from dao.Customers import Customers
from dao.Inventory import Inventory
from dao.OrderDetails import OrderDetails
from dao.Orders import Orders
from dao.Products import Products
from exceptions.CustomError import CustomError
from exceptions.InsufficientStockException import InsufficientStockException
from exceptions.InvalidDataException import InvalidEmailError
from exceptions.InvalidIDError import InvalidIDError
from exceptions.InvalidNameError import InvalidNameError
from exceptions.InvalidPhoneError import InvalidPhoneError
from exceptions.InvalidPriceError import InvalidPriceError
from exceptions.InvalidQuantityError import InvalidQuantityError

condition = True
create = True
try:

    while condition:
        customers1 = Customers()
        products1 = Products()
        orders1 = Orders()
        orderdetails1 = OrderDetails()
        inventory1 = Inventory()

        while create:
            customers1.create()
            products1.create()
            orders1.create()
            print(" New column is added later. So call AlterTable().")
            orderdetails1.create()
            inventory1.create()
            create = False

        print("select table")
        print("1.Customers\n2.Products\n3.Orders\n4.OrderDetails\n5.Inventory\n6.Exit")

        choice = int(input("enter your choice"))
        if choice == 1:
            while True:
                print(
                    "1.Add customer\t2.View Customers Data\t3.Update Customer Data\n4.Delete Customer Data\t5.Get "
                    "Customer Details by ID\t6.Calculate Total Orders\n7.Exit")
                choice = int(input("enter your choice"))
                if choice == 1:
                    customers1.addCustomer()
                elif choice == 2:
                    customers1.select()
                elif choice == 3:
                    customers1.UpdateCustomerInfo()
                elif choice == 4:
                    customers1.delete()
                elif choice == 5:
                    cid = int(input("enter customer ID"))
                    customers1.GetCustomerDetails(cid)
                elif choice == 6:
                    cid = int(input("enter customer ID"))
                    customers1.CalculateTotalOrders(cid)
                else:
                    break
        elif choice == 2:
            while True:
                print("1.Add Product\t2.View Product Details\t3.Update Product Details\n4.Delete Product\t5.Get Product"
                      "by ID\t6.Check for availability\n7.Exit")
                choice = int(input("enter your choice"))
                if choice == 1:
                    products1.addProduct()
                elif choice == 2:
                    products1.selectProducts()
                elif choice == 3:
                    products1.UpdateProductInfo()
                elif choice == 4:
                    products1.deleteProduct()
                elif choice == 5:
                    pid = int(input("enter product ID"))
                    products1.GetProductDetails(pid)
                elif choice == 6:
                    pid = int(input("enter product ID"))
                    print(products1.IsProductInStock(pid))
                else:
                    break
        elif choice == 3:
            while True:
                print("1.Add Order\t2.View Order Details\t3.Update Order Details\n4.Delete Order\t5.Get Order"
                      "by ID\t6.Update Order Status\n7.Calculate Amount for Order\t8.Cancel Order\t9.Exit")
                choice = int(input("enter your choice"))
                if choice == 1:
                    orders1.addOrder()
                elif choice == 2:
                    orders1.selectOrders()
                elif choice == 3:
                    orders1.updateOrder()
                elif choice == 4:
                    orders1.deleteOrder()
                elif choice == 5:
                    oid = int(input("enter order ID"))
                    orders1.GetOrderDetails(oid)
                elif choice == 6:
                    oid = int(input("enter order ID"))
                    status = input("enter new status")
                    orders1.UpdateOrderStatus(oid, status)
                elif choice == 7:
                    orders1.CalculateTotalAmount()
                elif choice == 8:
                    oid = int(input("enter order ID"))
                    orders1.CancelOrder(oid)
                else:
                    break
        elif choice == 4:
            while True:
                print(
                    "1.Add Details for Order\t2.View OrderDetails Data\t3.Update OrderDetails Data\n4.Delete "
                    "OrderDetails Data\t5.Get OrderDetails  by ID\t6.Calculate CalculateSubtotal\n7.Add "
                    "discount\t8.View Sales Report\t9.Exit")
                choice = int(input("enter your choice"))
                if choice == 1:
                    orderdetails1.addOrderDetail()
                elif choice == 2:
                    orderdetails1.selectOrderDetails()
                elif choice == 3:
                    orderdetails1.updateOrderDetail()
                elif choice == 4:
                    orderdetails1.deleteOrderDetail()
                elif choice == 5:
                    cid = int(input("enter OrderDetails ID"))
                    orderdetails1.GetOrderDetails(cid)
                elif choice == 6:
                    orderdetails1.CalculateSubtotal()
                elif choice == 7:
                    dis = int(input("enter discount"))
                    orderdetails1.AddDiscount(dis)
                elif choice == 8:
                    orderdetails1.SalesReporting()
                else:
                    break
        elif choice == 5:
            while True:
                print(
                    "1.Add Inventory data\t2.View Inventory Data\t3.Update Inventory Data\n4.Delete Inventory "
                    "Data\t5.Get Inventory Details  by ID\t6.Get Quantity available for a ID\n7. Add quantity To "
                    "Inventory\t8.Remove quantity from Inventory\t9.Update Quantity to inventory\n10.Check product "
                    "availability\t11.Value of Inventory\t12.Know the low stock products\n13.Know the out of stock "
                    "products\t14.Exit")
                choice = int(input("enter your choice"))
                if choice == 1:
                    inventory1.addInventory()
                elif choice == 2:
                    inventory1.selectInventory()
                elif choice == 3:
                    inventory1.updateInventory()
                elif choice == 4:
                    inventory1.deleteInventory()
                elif choice == 5:
                    inventory1.GetProduct()
                elif choice == 6:
                    inventory1.GetQuantityInStock()
                elif choice == 7:
                    inventory1.AddToInventory()
                elif choice == 8:
                    inventory1.RemoveFromInventory()
                elif choice == 9:
                    inventory1.UpdateStockInventory()
                elif choice == 10:
                    inventory1.IsProductAvailable()
                elif choice == 11:
                    inventory1.GetInventoryValue()
                elif choice == 12:
                    inventory1.ListLowStockProducts()
                elif choice == 13:
                    inventory1.ListOutOfStockProducts()
                else:
                    break
        else:
            break
except CustomError as e:
    print(e)
except InsufficientStockException as e:
    print(e)
except InvalidEmailError as e:
    print(e)
except InvalidIDError as e:
    print(e)
except InvalidNameError as e:
    print(e)
except InvalidPhoneError as e:
    print(e)
except InvalidPriceError as e:
    print(e)
except InvalidQuantityError as e:
    print(e)
except Exception as e:
    print(e)
