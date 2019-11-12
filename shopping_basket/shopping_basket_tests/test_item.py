# coding=utf-8

import unittest

from basket_pricer.item import Item, NegativePriceError

class ItemTests(unittest.TestCase):

    def test_item_initialised(self):
        ''' Test that we can create item object passing all required arguments.
            As a result we should get properly initialised object.
        '''
        beans = Item('Beans', 1.56)
        self.assertEqual(beans.name, 'Beans')
        self.assertEqual(beans.price, 1.56)
        self.assertEqual(str(beans), 'Beans, £1.56')
        self.assertEqual(repr(beans), '<Item: name=Beans price=1.56 discounts=[]>')

    def test_item_missing_argument(self):
        ''' Test that we get an exception when we try to create an item,
            without required arguments.
        '''
        with self.assertRaises(TypeError):
            _ = Item(name='Pasta')
            
        with self.assertRaises(TypeError):
            _ = Item(price=1.56)

    def test_item_throw_exception_when_price_negative(self):
        with self.assertRaises(NegativePriceError):
            _ = Item('Salmon', -20.24)