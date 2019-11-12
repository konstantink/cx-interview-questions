# coding=utf-8


from typing import List, Tuple, Union

from basket_pricer.item import Item


class DuplicateItemError(Exception):
    pass


class ItemNotFoundError(Exception):
    pass


class Catalogue(dict):

    def __init__(self, *args: Union[Tuple[str, float], Item]) -> None:
        ''' Initialises Catalogue either empty or with some pre-defined items.

            :param args: should be the sequence of Items or tuples of values for
                         Item creation, i.e. (name, price)
        '''
        for arg in args:
            if isinstance(arg, Item):
                self.add_item(arg)
            elif isinstance(arg, tuple):
                self.add_item(Item(*arg))

    def add_item(self, item: Item) -> None:
        ''' Adds item to the catalogue.

            :param item: Item to add
        '''
        if item.name in self:
            raise DuplicateItemError('Item {} is already in catalogue'.format(item.name))

        self[item.name] = item

    def add_items(self, items: List[Item]) -> None:
        ''' Adds items to catalogue.

            :param items: List of Items
        '''
        for item in items:
            self.add_item(item)

    def get_items(self) -> List[Item]:
        ''' Returns the list of items in the catalogue.

            :return list of Items
        '''
        return self.values()

    def get_item(self, item: str) -> Item:
        ''' Returns the list of items in the catalogue.

            :return list of Items
        '''
        return self.get(item)

    def remove_item(self, item: Union[str, Item]) -> None:
        ''' Removes item from catalogue.

            :param item: Item to remove
        '''
        if isinstance(item, Item) and item.name in self:
            removed = self.pop(item.name)
        elif isinstance(item, str) and item in self:
            removed = self.pop(item)
        else:
            raise ItemNotFoundError("Item '{}' not found in catalogue".format(removed.name))

    def is_item_in(self, item: Union[str, Item]) -> bool:
        ''' Checks if item is added to catalogue.

            :param item: Item to check
            :returns bool True if item is in catalogue or False if not
        '''
        return (isinstance(item, Item) and item.name in self) or (isinstance(item, str) and item in self)

    def __str__(self) -> str:
        return '{} products'.format(len(self))

    def __repr__(self) -> str:
        return '<Catalogue products={}>'.format(len(self))