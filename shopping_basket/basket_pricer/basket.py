# coding=utf-8

from typing import List, TypeVar, Union

from basket_pricer.item import Item
from basket_pricer.utility import round_up


T = TypeVar('T')


class NotInCatalogueError(Exception):
    pass


class Basket(dict):

    def __init__(self, catalogue):
        ''' Inits the Basket instance with the catalogue of available products.

            :param catalogue: Catalogue
        '''
        self.catalogue = catalogue
        self.discounts = []

    def subtotal(self) -> float:
        ''' Calculates total sum of all items in the basket excluding discounts.

            :returns float: Total sum of all items in basket
        '''
        return round_up(float(sum(item.price * n for item, n in self.items())))

    def discount(self) -> float:
        ''' Calculates discount that should be reduced from subtotal.

            :returns float: Total discount to reduce from subtotal
        '''
        discount = 0.0
        for d in self.get_discounts():
            discount = d.calculate_discount(basket=self)
        return discount

    def total(self) -> float:
        ''' Calculates total sum to pay, i.e. sum excluding discounts.

            :returns float: Total sum to pay
        '''
        return round_up(self.subtotal() - self.discount())

    def get_discounts(self) -> List[T]:
        ''' Returns the list of discounts that should be applied on the items
            in the basket.
        '''
        return list(set(d for i in self.keys() for d in i.discounts))

    def add_item(self, item: Union[str, Item], n: int=1) -> None:
        ''' Checks if item is in catalogue and then add it to basket

            :param item: Item to add to basket
        '''
        name = item.name if isinstance(item, Item) else item
        if self.catalogue.is_item_in(name):
            product = self.catalogue.get_item(name)
            if product not in self:
                self[product] = 0
            self[product] += n
        else:
            raise NotInCatalogueError("Item '{}' is not in catalogue".format(name))

    def get_items(self) -> List[Item]:
        ''' Returns the list of items that are currently in the basket.

            :returns List[Item]: list of Items
        '''
        return self.keys()

    def remove_item(self, item: Union[str, Item]) -> None:
        ''' Checks if item is in catalogue and then add it to basket

            :param item: Item to add to basket
        '''
        name = item.name if isinstance(item, Item) else item
        if self.catalogue.is_item_in(name):
            if name not in self:
                self[name] = 0
            self[name] += 1

    def __repr__(self):
        return '<Basket: total_items={} unique_items={} discounts=[{}] subtotal={} discount={} total={}>'\
            .format(sum(self.values()), len(self.keys()), ','.join(d.name for d in self.discounts), self.subtotal(),
                self.discount(), self.total())