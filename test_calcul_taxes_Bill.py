''' Unit testing for the Bill class '''
import unittest # Note : An alternative Python test suite is 'pytest'
import calcul_taxes

class TestBill(unittest.TestCase):
    # Pre-computation of objects that could be used in multiple tests -> Faster testing.
    def setUp(self):
        self.valid_product = calcul_taxes.Product('test', 1, 1, False)

    def test_bad_types(self):
        ''' Checks that the method corretly discards invalid inputs '''

        # Invalid container
        test_input_containers = {'not iterable' :  123,
                                'bad iterable' : '123'}

        for name, i in test_input_containers.items():
            with self.subTest(name=name):
              with self.assertRaisesRegex(TypeError, "Invalid 'product_list' type. The product list must be a list of Product instances !"):
                calcul_taxes.Bill(i)

        # Empty list
        with self.assertRaisesRegex(ValueError, "Empty 'product_list'. The product list must contain Product instances !"):
           calcul_taxes.Bill([])

        # Invalid elements in non-empty container
        test_input_elements = {'uninitialized product' :  [calcul_taxes.Product],
                               'invalid object object' :  [self.valid_product, '123', 1]}

        for name, i in test_input_elements.items():
            with self.subTest(name=name):   
                with self.assertRaisesRegex(TypeError, "Invalid 'product_list' elements. The product list must only contain Product instances !"):
                  calcul_taxes.Bill([calcul_taxes.Product])

    def test_result(self):
        # Dependency on an external 'production' file - but I'd argue it is acceptable for testing (... I mean, for this technical test)
        test_bills = {calcul_taxes.bill1 : {'sum_tax':1.50, 'total': 29.89},
                      calcul_taxes.bill2 : {'sum_tax':7.65, 'total': 65.15},
                      calcul_taxes.bill3 : {'sum_tax':6.70, 'total': 74.68}}

        for bill, o in test_bills.items():
            bill.sum_tax = o['sum_tax']
            bill.total   = o['total']

if __name__ == '__main__':
    unittest.main(exit=False)

# Note : Integration testing would be necessary when dealing with more complex code bases.