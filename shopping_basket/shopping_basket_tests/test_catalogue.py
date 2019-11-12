# coding=utf-8

import unittest

from basket_pricer.catalogue import Catalogue, DuplicateItemError
from basket_pricer.item import Item

class CatalogueTests(unittest.TestCase):

    def test_catalogue_initialised(self):
        ''' Test we can create a Catalogue object.
        '''
        catalogue = Catalogue()
        self.assertEqual(str(catalogue), '0 products')

    def test_catalogue_add_item(self):
        ''' Test we can add Item to catalogue.
        '''
        catalogue = Catalogue()
        pepsi = Item('Pepsi 1.5L', 1.5)
        catalogue.add_item(pepsi)
        self.assertEqual(str(catalogue), '1 products')

    def test_catalogue_duplicate_items(self):
        ''' Test we can't add the same item to the catalogue twice.
            We expect to get an exception about duplication
        '''
        catalogue = Catalogue()
        sardines = Item('Sardines', 5.75)

        with self.assertRaises(DuplicateItemError):
            catalogue.add_item(sardines)
            catalogue.add_item(Item('Sardines', 3.25))

    def test_catalogue_init_with_items(self):
        ''' Test we can create Catalogue object passing Items or tuples (name, price).
        '''
        groceries = Catalogue(('Potatoes', 0.89), ('Tomatoes', 1.29), ('Beef', 5.45))
        self.assertEqual(str(groceries), '3 products')

        bathroom_cleaner = Item('Cleanser 750ml', 1.)
        toilet_duck = Item('Toilet Duck Citrus 750ml', 1.25)
        household_goods=Catalogue(bathroom_cleaner, toilet_duck)
        self.assertEqual(str(household_goods), '2 products')

    def test_catalogue_get_items(self):
        ''' Test we can get the list of items currently added to catalogue
        '''
        groceries = Catalogue(('Potatoes', 0.89), ('Tomatoes', 1.29), ('Beef', 5.45))
        items = list(sorted(groceries.get_items(), key=lambda x: x.price))
        self.assertEqual(items, [Item('Potatoes', 0.89), Item('Tomatoes', 1.29), Item('Beef', 5.45)])

        empty_catalogue = Catalogue()
        self.assertEqual(list(empty_catalogue.get_items()), [])