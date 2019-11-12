# coding=utf-8

from typing import List

from basket_pricer.basket import Basket
from basket_pricer.catalogue import Catalogue
from basket_pricer.item import Item
from basket_pricer.utility import round_up


class PercentageValueError(Exception):
    pass


class ItemsNumberError(Exception):
    pass


class ArgumentError(Exception):
    pass


class Discount:

    _instances = {}

    def __init__(self):
        ''' Inits base class Discount, it creates a Catalogue instance, which
            is basically a collection of items that are assigned current discount.
        '''
        self.catalogue = Catalogue()

    def add_item(self, item: Item) -> None:
        ''' Adds item to the discount, as we need to know what products have this
            kind of discount, to be able to suggest to the user the list of available
            product for this particular kind of discount.

            :param item: Item to associate with current discount
        '''
        self.catalogue.add_item(item)

    def remove_item(self, item: Item) -> None:
        ''' Removes item from the discount

            :param item: Item to remove from discount
        '''
        self.catalogue.remove_item(item)

    def calculate_discount(self, **kwargs):
        raise NotImplementedError('Should be implemented in child classes')


class PercentageDiscount(Discount):

    def __new__(cls, percentage: float=0.0):
        instance = super().__new__(cls)
        cls._instances[percentage] = instance
        return instance

    def __init__(self, percentage: float=0.0):
        ''' Constructor for PercentageDiscount type.

            :param percentage: amount of the discount, should be betwenn 0 and 1.
                               in other case instance wouldn't be created.
        '''
        super().__init__()
        if percentage > 1.0 or percentage < 0.0:
            self._instances.pop(percentage)
            raise PercentageValueError('Percentage is expected to be in rage [0, 1]')
        self.percentage = percentage
        self.name = '{}%Off'.format(int(self.percentage * 100))

    @classmethod
    def get_or_create(cls, percentage):
        if percentage not in cls._instances:
            cls._instances[percentage] = cls(percentage)
        return cls._instances[percentage]

    def __repr__(self) -> str:
        return '<PercentageDiscount: percentage={} name={} products={}>'\
            .format(self.percentage, self.name, len(self.catalogue))

    def calculate_discount(self, basket, **kwargs) -> float:
        ''' Calculates discount for products.

            :param basket: Basket with all added items
            :returns float: sum of discount, i.e. what should be substracted from subtotal
        '''
        discount = 0.0
        items_on_discount = set(self.catalogue.get_items())
        for item, n in basket.items():
            if item in items_on_discount:
                discount += round_up(float(item.price * self.percentage * n), 2)

        return discount


class BuyNGet1FreeDiscount(Discount):

    def __new__(cls, n: int):
        instance = super().__new__(cls)
        cls._instances[n] = instance
        return instance

    def __init__(self, n: int) -> None:
        ''' Constructor for PercentageDiscount type.

            :param n: number of products to buy to get free one.
        '''
        super().__init__()
        if n < 0 or not isinstance(n, int):
            raise ItemsNumberError('Expected n to be positive integer, got {}'.format('negative' if n < 0 else type(n)))
        self.n = n
        self.name = 'Buy{}Get1Free'.format(self.n)

    @classmethod
    def get_or_create(cls, n):
        if n not in cls._instances:
            cls._instances[n] = cls(n)
        return cls._instances[n]

    def __repr__(self) -> str:
        return '<BuyNGet1FreeDiscount: n={} name={} products={}>'.format(self.n, self.name, len(self.catalogue))

    def calculate_discount(self, basket: Basket, **kwargs) -> float:
        ''' Calculates discount for products.

            :param basket: Basket with all added items
            :returns float: sum of discount, i.e. what should be substracted from subtotal
        '''
        discount = 0.0
        items_on_discount = set(self.catalogue.get_items())
        for item, n in basket.items():
            if item in items_on_discount and n >= self.n:
                discount += round_up(float(item.price * int((n / (self.n+1)))), 2)

        return discount


class BuyNOfGetCheapestFreeDiscount(Discount):

    def __new__(cls, n: int):
        instance = super().__new__(cls)
        cls._instances[n] = instance
        return instance

    def __init__(self, n: int) -> None:
        ''' Constructor for PercentageDiscount type.

            :param n: number of products to buy to get free one
            :param items: list of available items.
        '''
        super().__init__()
        self.n = n
        self.name = 'Buy{}OfGetCheapestFree'.format(self.n)

    def __repr__(self) -> str:
        return '<BuyNOfGetCheapestFreeDiscount: n={} name={} products={}>'\
            .format(self.n, self.name, len(self.catalogue))

    @classmethod
    def get_or_create(cls, n:int):
        if n not in cls._instances:
            cls._instances[n] = cls(n)
        return cls._instances[n]

    def calculate_discount(self, basket: Basket, **kwargs) -> float:
        ''' Calculates discount for products.

            :param basket: Basket with all added items
            :returns float: sum of discount, i.e. what should be substracted from subtotal
        '''
        discounted_items = []
        items_on_discount = set(self.catalogue.get_items())
        for item, quantity in basket.items():
            if item in items_on_discount:
                discounted_items.extend(((item.name, item.price),) * quantity)

        discounted_items = sorted(discounted_items, key=lambda x: x[1], reverse=True)

        discount = sum(i[1] for i in discounted_items[self.n-1::self.n])

        return discount