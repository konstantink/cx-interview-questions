# coding=utf-8

import unittest

import basket_pricer.discount as discount

from basket_pricer.basket import Basket
from basket_pricer.catalogue import Catalogue
from basket_pricer.item import Item


class BasketTests(unittest.TestCase):

    def test_basket_init(self):
        ''' Test we can init Basket instance.
        '''
        basket = Basket(Catalogue())
        self.assertEqual(repr(basket),
            '<Basket: total_items=0 unique_items=0 discounts=[] subtotal=0.0 discount=0.0 total=0.0>')

    def test_basket_add_item(self):
        ''' Test we can add item to the basket
        '''
        sandwich = Item('Turkey Sandwich', 1.8)
        basket = Basket(Catalogue(sandwich))

        # Test we can add item to basket using Item instance
        basket.add_item(sandwich)
        self.assertEqual(repr(basket),
            '<Basket: total_items=1 unique_items=1 discounts=[] subtotal=1.8 discount=0.0 total=1.8>')

        # Test we can add item to basket using name
        basket.add_item('Turkey Sandwich')
        self.assertEqual(repr(basket),
            '<Basket: total_items=2 unique_items=1 discounts=[] subtotal=3.6 discount=0.0 total=3.6>')

    def test_get_discounts(self):
        ''' Test we can get the list of discounts that should be applied to items in basket
        '''
        sandwich = Item('Turkey Sandwich', 1.8)
        basket = Basket(Catalogue(sandwich))
        basket.add_item(sandwich)
        self.assertEqual(basket.get_discounts(), [])

        sandwich.add_discount(discount.PercentageDiscount(0.25))
        self.assertEqual(basket.get_discounts(), [discount.PercentageDiscount.get_or_create(0.25)])

        sandwich.add_discount(discount.BuyNGet1FreeDiscount(3))
        self.assertIn(discount.BuyNGet1FreeDiscount.get_or_create(3), basket.get_discounts())
        self.assertIn(discount.PercentageDiscount.get_or_create(0.25), basket.get_discounts())
        self.assertEqual(len(basket.get_discounts()), 2)

    def test_basket_case1(self):
        ''' Test we calculate properly subtotal, discount and total
        '''
        catalogue = Catalogue(('Baked beans', 0.99), ('Biscuits', 1.2), ('Sardines', 1.89), ('Shampoo (Small)', 2),
            ('Shampoo (Medium)', 2.5), ('Shampoo (Large)', 3.5))
        basket = Basket(catalogue)
        Item.get_or_create('Baked beans', 0.99).add_discount(discount.BuyNGet1FreeDiscount(2))
        Item.get_or_create('Sardines', 1.89).add_discount(discount.PercentageDiscount(0.25))

        basket.add_item(Item.get_or_create('Baked beans', 0.99), n=4)
        basket.add_item(Item.get_or_create('Biscuits', 1.2), n=1)

        self.assertEqual(basket.subtotal(), 5.16)
        self.assertEqual(basket.discount(), 0.99)
        self.assertEqual(basket.total(), 4.17)

    def test_basket_case2(self):
        ''' Test we calculate properly subtotal, discount and total
        '''
        catalogue = Catalogue(('Baked beans', 0.99), ('Biscuits', 1.2), ('Sardines', 1.89), ('Shampoo (Small)', 2),
            ('Shampoo (Medium)', 2.5), ('Shampoo (Large)', 3.5))
        basket = Basket(catalogue)
        Item.get_or_create('Baked beans', 0.99).add_discount(discount.BuyNGet1FreeDiscount(2))
        Item.get_or_create('Sardines', 1.89).add_discount(discount.PercentageDiscount(0.25))

        basket.add_item(Item.get_or_create('Baked beans', 0.99), n=2)
        basket.add_item(Item.get_or_create('Biscuits', 1.2), n=1)
        basket.add_item(Item.get_or_create('Sardines', 1.89), n=2)

        self.assertEqual(basket.subtotal(), 6.96)
        self.assertEqual(basket.discount(), 0.95)
        self.assertEqual(basket.total(), 6.01)

    def test_basket_case3(self):
        ''' Test we calculate properly subtotal, discount and total
        '''
        catalogue = Catalogue(('Shampoo (Small)', 2), ('Shampoo (Medium)', 2.5), ('Shampoo (Large)', 3.5))
        basket = Basket(catalogue)
        discount_ = discount.BuyNOfGetCheapestFreeDiscount.get_or_create(3)
        Item.get_or_create('Shampoo (Small)', 2).add_discount(discount_)
        Item.get_or_create('Shampoo (Medium)', 2.5).add_discount(discount_)
        Item.get_or_create('Shampoo (Large)', 3.5).add_discount(discount_)

        basket.add_item(Item.get_or_create('Shampoo (Small)', 2), n=2)
        basket.add_item(Item.get_or_create('Shampoo (Medium)', 2.5), n=3)
        basket.add_item(Item.get_or_create('Shampoo (Large)', 3.5), n=3)

        self.assertEqual(basket.subtotal(), 22.0)
        self.assertEqual(basket.discount(), 6.0)
        self.assertEqual(basket.total(), 16.0)