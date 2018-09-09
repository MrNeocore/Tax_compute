import math
import warnings

class Product:
    tax_categories = {'book':0, 'medicine':0, 'food':0, 'others':10}

    def __init__(self, name, count, unit_excl_tax, imported, tax_category='others'):

        # Checks that the input price is either an integer or a floating point value. We could also add the Decimal type...
        if not isinstance(unit_excl_tax, (int, float)):
            raise TypeError("Invalid 'unit_excl_tax' type. Price ex-VAT must be an integer or floating point variable !")

        # Checks that the price is non negative
        if unit_excl_tax <= 0.0:
            raise ValueError("Invalid 'unit_excl_tax' value. The item price (without taxes) must be a positive number !")

        # Cheks that the object count is an integer
        if not isinstance(count, int):
            raise TypeError("Invalid 'count' type. The item count must be a (positive) integer number !")

        # Cheks that the object count is strictly positive
        if count < 1:
            raise ValueError("Invalid 'count' value. The item count must be a (positive) integer number !")

        # Checks that the object tax category is valid. Alternatively, if it doesn't exist, we could default to 'others' (taxed). 
        if tax_category not in Product.tax_categories:
            raise ValueError(f"Invalid 'tax_category' value. Supported tax categories are : {list(Product.tax_categories.keys())}")

        # Checks that the input flag is valid. (very useful comment, I know)
        if imported not in [True, False]: # 0 and 1 evaluate to True / False and are therefore valid inputs. 
            raise TypeError("Invalid 'imported' type. The 'imported' parameter must be a boolean flag !")

        # No constraits on the 'name' parameter, as all Python objects are str()-able (absence of __str__), so checks are not necessary.
        # Of course, a string is the most logical type to use.
        self.name = str(name)
        self.count = count
        self.unit_excl_tax = unit_excl_tax
        self.imported = imported

        # Product tax ('immutable')
        self._product_tax = Product.tax_categories[tax_category] 

    # Simply return (when calling print()) the product string containing its count, its name whether or not it is imported, along with its unit tax included price.  
    def __str__(self):
        out = f"{self.count} {self.name}" 
        if self.imported:
            out += ' importé(e)'
        out += f" : {self.total_incl_tax:.2f}"

        return out

    @classmethod
    def tax_round(self, tax):
        return math.ceil(tax / 0.05) * 0.05

    # Note : To avoid unecessary recomputation, we could track the 'dirty' state of the object. 
    # However, in this case, the loss of code clarity isn't worth the performance improvement.
    @property
    def total_excl_tax(self):
        return round(self.unit_excl_tax * self.count, 2)
    
    @property
    def unit_incl_tax(self):
        return round(self.unit_excl_tax + self.unit_taxes, 2)

    @property
    def total_incl_tax(self):
        return round(self.unit_incl_tax * self.count, 2)
    
    @property
    def unit_taxes(self):
        tax_rate = self._product_tax
        if self.imported:
            tax_rate += 5

        return round(self.tax_round(self.unit_excl_tax*tax_rate/100), 2)

    @property
    def total_taxes(self):
        return round(self.unit_taxes * self.count, 2)
    

class Bill:
    def __init__(self, product_list):
        # Cheks that the input is a list
        if not isinstance(product_list, list):
            raise TypeError("Invalid 'product_list' type. The product list must be a list of Product instances !")

        # Checks that the list is not empty
        if not len(product_list):
            raise ValueError("Empty 'product_list'. The product list must contain Product instances !")

        # Checks that all elements in the list are of type Product
        if not all([isinstance(x, Product) for x in product_list]):
            raise TypeError("Invalid 'product_list' elements. The product list must only contain Product instances !")

        # 'Hidden' attribute as it is not meant to be changed - Bill object considered immutable.
        self._product_list = product_list

        # Not a fan of having computation in constructors, but it isn't a big deal in this case.
        self.sum_tax = sum([product.total_taxes for product in self._product_list])
        self.sum_exc = sum([product.total_excl_tax for product in self._product_list])
        self.total = self.sum_exc + self.sum_tax

    # Called when 'print()'-int the object - simply building a string containing product information, total tax amount and total price.
    def __str__(self):
        bill_str = ["===== Products bill ====="]

        bill_str.extend([str(product) for product in self._product_list])
        bill_str.append(f"Montant des taxes : {self.sum_tax:.2f}")
        bill_str.append(f"Total : {self.total:.2f}")

        bill_str.append("=========================\n")

        return '\n'.join(bill_str)

# ================================================
# Bill 1
products1 = [Product(name='livre', 
                     count=1, 
                     unit_excl_tax=12.49,
                     imported=False,
                     tax_category='book'),

             Product(name='CD musical', 
                     count=1, 
                     unit_excl_tax=14.99,
                     imported=False),

             Product(name='barre de chocolat', 
                     count=1, 
                     unit_excl_tax=0.85,
                     imported=False,
                     tax_category='food')]

bill1 = Bill(products1)

# Bill 2
products2 = [Product(name='boîte de chocolat', 
                     count=1, 
                     unit_excl_tax=10.00,
                     imported=True,
                     tax_category='food'),

             Product(name='flacon de parfum', 
                     count=1,
                     unit_excl_tax=47.50,
                     imported=True)]

bill2 = Bill(products2)

# Bill 3
products3 = [Product(name='flacon de parfum', 
                     count=1,
                     unit_excl_tax=27.99,
                     imported=True),

             Product(name='flacon de parfum', 
                     count=1,
                     unit_excl_tax=18.99,
                     imported=False),

             Product(name='boîte de pilules contre la migraine', 
                     count=1,
                     unit_excl_tax=9.75,
                     imported=False,
                     tax_category='medicine'),

             Product(name='boîte de chocolats', 
                     count=1,
                     unit_excl_tax=11.25,
                    imported=True,
                    tax_category='food')]

bill3 = Bill(products3)


if __name__ == '__main__':    
    print(bill1)
    print(bill2)
    print(bill3)