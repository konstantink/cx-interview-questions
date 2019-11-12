# coding=utf-8

import unittest

import basket_pricer.discount as uut

from basket_pricer.basket import Basket
from basket_pricer.catalogue import Catalogue
from basket_pricer.item import Item


class PercentageDiscountTests(unittest.TestCase):

    def test_init(self):
        ''' Test we can create PercentageDiscount instance.
        '''
        discount = uut.PercentageDiscount(0.34)
        self.assertEqual(repr(discount), '<PercentageDiscount: percentage=0.34 name=34%Off products=0>')

        # Test border values
        discount0 = uut.PercentageDiscount(0.0)
        self.assertEqual(repr(discount0), '<PercentageDiscount: percentage=0.0 name=0%Off products=0>')

        discount1 = uut.PercentageDiscount(1.0)
        self.assertEqual(repr(discount1), '<PercentageDiscount: percentage=1.0 name=100%Off products=0>')

    def test_init_incorrect_value(self):
        ''' Test we can't create PercentageDiscount instance if we provide improper value
            of the discount. In that case we expect to get an exception saying that.
        '''
        with self.assertRaises(uut.PercentageValueError):
            _ = uut.PercentageDiscount(1.01)

        with self.assertRaises(uut.PercentageValueError):
            _ = uut.PercentageDiscount(-0.0001)

    def test_add_product(self):
        ''' Test we can add product to the discount.
        '''
        discount = uut.PercentageDiscount(0.25)
        discount.add_item(Item('Nappies 80', 8))
        self.assertEqual(repr(discount), '<PercentageDiscount: percentage=0.25 name=25%Off products=1>')

    def test_calculate_discount(self):
        ''' Test we properly calculate discount.
        '''
        discount = uut.PercentageDiscount(0.1)
        basket = Basket(Catalogue(Item.get_or_create('Chocolatery swirls', 0.99)))
        Item.get_or_create('Chocolatery swirls', 0.99).add_discount(discount)
        basket.add_item(Item.get_or_create('Chocolatery swirls', 0.99), n=1)
        self.assertEqual(discount.calculate_discount(basket), 0.1)


class BuyNGet1FreeDiscountTests(unittest.TestCase):

    def test_init(self):
        ''' Test we can create PercentageDiscount instance.
        '''
        discount = uut.BuyNGet1FreeDiscount(n=3)
        self.assertEqual(repr(discount), '<BuyNGet1FreeDiscount: n=3 name=Buy3Get1Free products=0>')

    def test_init_incorrect_value(self):
        ''' Test we can't create BuyNGet1FreeDiscount instance if we provide improper value
            of the discount. In that case we expect to get an exception saying that.
        '''
        with self.assertRaises(uut.ItemsNumberError):
            _ = uut.BuyNGet1FreeDiscount(1.01)

        with self.assertRaises(uut.ItemsNumberError):
            _ = uut.BuyNGet1FreeDiscount(-12)

    def test_add_product(self):
        ''' Test we can add product to the discount.
        '''
        discount = uut.BuyNGet1FreeDiscount(4)
        discount.add_item(Item('Nappies 80', 8))
        self.assertEqual(repr(discount), '<BuyNGet1FreeDiscount: n=4 name=Buy4Get1Free products=1>')

    def test_calculate_discount(self):
        ''' Test we properly calculate discount.
        '''
        discount = uut.BuyNGet1FreeDiscount(2)
        basket = Basket(Catalogue(Item.get_or_create('Mackerel', 3.6)))
        Item.get_or_create('Mackerel', 3.6).add_discount(discount)
        basket.add_item(Item.get_or_create('Mackerel', 3.6), n=3)
        self.assertEqual(discount.calculate_discount(basket), 3.6)

        basket.add_item(Item.get_or_create('Mackerel', 3.6), n=2)
        self.assertEqual(discount.calculate_discount(basket), 3.6)

        basket.add_item(Item.get_or_create('Mackerel', 3.6), n=1)
        self.assertEqual(discount.calculate_discount(basket), 7.2)

        basket.add_item(Item.get_or_create('Mackerel', 3.6), n=1)
        self.assertEqual(discount.calculate_discount(basket), 7.2)