''' Unit testing for the Product class '''
import unittest # Note : An alternative Python test suite is 'pytest'
import calcul_taxes

class TestProduct(unittest.TestCase):
    def setUp(self):
        self.valid_count = 1
        self.invalid_count_types = ['a', []]
        self.invalid_count_values = [-1, 0]
        self.valid_price_value = 12.0
        self.invalid_price_types = [1+1j, '12']
        self.invalid_price_values = [0.0, -12.0]
        self.valid_import_flag = True
        self.invalid_import_flag_types = ['Yes'] 
        self.valid_tax_categories = calcul_taxes.Product.tax_categories
        self.invalid_tax_categories = ['drinks', None, 2]

    def loop_assertRaises(self, var_name, inputs, exception, msg_regex="*"):
        product_input =  {'name':'test', 'count':self.valid_count, 'unit_excl_tax':self.valid_price_value, 'imported':self.valid_import_flag, 'tax_category':next(iter(self.valid_tax_categories.keys()))}
        assert(var_name in product_input) # Should we unit test the unit testing code ? :D

        for i in inputs:
            product_input[var_name] = i
            with self.subTest(name=product_input):
                with self.assertRaisesRegex(exception, msg_regex):
                    calcul_taxes.Product(**product_input)


    def loop_assertEqual(self, inputs_outputs):
        for i, o in inputs_outputs:
            with self.subTest(name=i):
                prd = calcul_taxes.Product(name='test', **i)
                self.assertEqual([prd.unit_excl_tax, prd.total_excl_tax, prd.unit_taxes, prd.total_taxes, prd.unit_incl_tax, prd.total_incl_tax], o)


    def test_bad_types(self):
        ''' Checks that the method corretly discards invalid inputs '''

        # Test invalid price type
        self.loop_assertRaises('unit_excl_tax', self.invalid_price_types, TypeError, "Invalid 'unit_excl_tax' type. Price ex-VAT must be an integer or floating point variable !")
        
        # Test invalid price value
        self.loop_assertRaises('unit_excl_tax', self.invalid_price_values, ValueError, "Invalid 'unit_excl_tax' value. The item price \(without taxes\) must be a positive number !")

        # Test invalid count types
        self.loop_assertRaises('count', self.invalid_count_types, TypeError, "Invalid 'count' type. The item count must be a \(positive\) *integer number !*")
        
        # Test invalid count values
        self.loop_assertRaises('count', self.invalid_count_values, ValueError, "Invalid 'count' value. The item count must be a \(positive\) integer number !")
        
        # Test imported types
        self.loop_assertRaises('imported', self.invalid_import_flag_types, TypeError, "Invalid 'imported' type. The 'imported' parameter must be a boolean flag !")

        # Test invalid categories
        self.loop_assertRaises('tax_category', self.invalid_tax_categories, ValueError, "Invalid 'tax_category' value. Supported tax categories are :*")
        

    def test_results(self):
        ''' Checks that the Product class behaves as intended using valid inputs '''
        # Output format : [unit_excl_tax, total_excl_tax, unit_taxes, total_taxes, unit_incl_tax, total_incl_tax]
        inputs_outputs = [({'count':1, 'unit_excl_tax':1.0, 'imported':False, 'tax_category':'food'}     ,   [1.0, 1.0, 0.0 , 0.0 , 1.0 , 1.0]),
                          ({'count':1, 'unit_excl_tax':1.0, 'imported':False, 'tax_category':'others'}   ,   [1.0, 1.0, 0.1 , 0.1 , 1.1 , 1.1]),
                          ({'count':1, 'unit_excl_tax':1.0, 'imported':True , 'tax_category':'medicine'} ,   [1.0, 1.0, 0.05, 0.05, 1.05, 1.05]),
                          ({'count':1, 'unit_excl_tax':1.0, 'imported':True , 'tax_category':'others'}   ,   [1.0, 1.0, 0.15, 0.15, 1.15, 1.15]),
                          ({'count':3, 'unit_excl_tax':1.0, 'imported':False, 'tax_category':'book'}     ,   [1.0, 3.0, 0.0 , 0.0 , 1.0 , 3.0]),
                          ({'count':3, 'unit_excl_tax':1.0, 'imported':False, 'tax_category':'others'}   ,   [1.0, 3.0, 0.1 , 0.3 , 1.1 , 3.3]),
                          ({'count':3, 'unit_excl_tax':1.0, 'imported':True , 'tax_category':'food'}     ,   [1.0, 3.0, 0.05, 0.15, 1.05, 3.15]),
                          ({'count':3, 'unit_excl_tax':1.0, 'imported':True , 'tax_category':'others'}   ,   [1.0, 3.0, 0.15, 0.45, 1.15, 3.45]),
                          ({'count':3, 'unit_excl_tax':2.1, 'imported':True , 'tax_category':'others'}   ,   [2.1, 6.3, 0.35, 1.05, 2.45, 7.35])] # Test correct rounding

        self.loop_assertEqual(inputs_outputs)

    def test_tax_categories(self):
        ''' Checks that the tax categories included in the Product class are correct - the usefulness of this test is debatable. '''
        inputs_outputs = {'food':0,
                          'medicine':0,
                          'book':0,
                          'others':10}

        # Test using a default valued Product instance
        for i, o in inputs_outputs.items():
            self.assertEqual(calcul_taxes.Product('test', 1, 1, False, i)._product_tax, o)

if __name__ == '__main__':
    unittest.main(exit=False)

# Note : Integration testing would be necessary when dealing with more complex code bases.