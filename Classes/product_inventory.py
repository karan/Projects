"""
Product Inventory Project - Create an application which manages
an inventory of products. Create a product class which has a
price, id, and quantity on hand. Then create an inventory class
which keeps track of various products and can sum up the inventory
value.
"""

class Product:

    def __init__(self, price, pid, qty):
        """
        Class constructor that needs a price, a product id,
        and quantity.
        """
        self.price = price
        self.pid = pid
        self.qty = qty

    def print_product(self):
        """
        Prints a single product.
        """
        print '%d\t%s\t%.02f each' % (self.pid, self.qty, self.price)

p = Product(1.4, 123, 5)
p.print_product()
