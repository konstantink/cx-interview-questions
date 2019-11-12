# coding=utf-8

from typing import Generic, TypeVar


T = TypeVar('T')

class NegativePriceError(Exception):
    pass


class Item(Generic[T]):
    _instances = {}

    def __new__(cls, name: str, price: float):
        instance = super().__new__(cls)
        cls._instances[(name, price)] = instance
        return instance

    def __init__(self, name: str, price: float) -> None:
        ''' Inits Item object. All arguments are required.
            :param name: Name of the item
            :param price: Price of the item. Should be positive, in case it's negative,
                           exception should be thrown. 
        '''
        if price < 0:
            self._instances.pop((name, price))
            raise NegativePriceError('Price cannot be negative')

        self.name = name
        self.price = price
        self.discounts = []

    @classmethod
    def get_or_create(cls, name: str, price: float) -> T:
        ''' Either retreives the instance from already created ones or
            create a new instance of Item class

            :params name: Item name
            :params price: Item price
        '''
        if (name, price) not in cls._instances:
            cls._instances[(name, price)] = cls(name, price)
        return cls._instances[(name, price)]

    def add_discount(self, discount) -> None:
        ''' Assigns discount to current item.

            :param discount: Discount to assign
        '''
        self.discounts.append(discount)
        discount.add_item(self)

    def remove_discount(self, discount) -> None:
        ''' Removes discount from item

            :param discount: Discount to remove
        '''
        self.discounts.remove(discount)
        discount.remove_item(self)

    def __hash__(self) -> str:
        return hash(self.name)

    def __eq__(self, other) -> bool:
        return self.name == other.name and self.price == other.price

    def __str__(self) -> str:
        return "{}, £{}".format(self.name, self.price)

    def __repr__(self) -> str:
        return "<Item: name={} price={} discounts=[{}]>"\
            .format(self.name, self.price, ','.join(str(d) for d in self.discounts))
