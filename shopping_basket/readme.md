## Shopping basket implementation

To execute tests use following command:

    python -m unittest discover shopping_basket_tests

**Note:** One test sometimes fails, that is something to investigate.

## Solution

There are four main classes: `Item`, `Catalogue`, `Discount`, `Basket`.

`Item` represents a product that is selling in the supermarket. It has 3 properties: `name`, `price` and `discounts`. Property `discounts` keeps references to all discount objects that were assigned to this product.

`Catalogue` is a collection of available items in the supermarket. It is implemented as a dictionary with the key as an `Item` name and value `Item` itself.

`Discount` is a base class for several types of discounts: `PercentageDiscount`, `BuyNGetOneFreeDiscount` and `BuyNOfGetCheapestFreeDiscount`. All these classes are responsible to calculate the discount for the `Basket`.

`Basket` is the main class that represents shopping basket. It is implemented as a dictionary where `Item` is a key and quantity is a value. It also accepts `Catalogue` instance as an input to know what products can be added to the basket. It implements interface: `subtotal()`, `discount()` and `total()`.

## Example

    import basket_pricer.discount as discount

    from basket_pricer.basket import basket
    from basket_pricer.catalogue import Catalogue
    from basket_pricer.item import Item


    catalogue = Catalogue(('Baked beans', 0.99), ('Biscuits', 1.2), ('Sardines', 1.89), ('Shampoo (Small)', 2),
        ('Shampoo (Medium)', 2.5), ('Shampoo (Large)', 3.5))
    basket = Basket(catalogue)

    Item.get_or_create('Baked beans', 0.99).add_discount(discount.BuyNGet1FreeDiscount(2))
    Item.get_or_create('Sardines', 1.89).add_discount(discount.PercentageDiscount(0.25))

    basket.add_item(Item.get_or_create('Baked beans', 0.99), n=2)
    basket.add_item(Item.get_or_create('Biscuits', 1.2), n=1)
    basket.add_item(Item.get_or_create('Sardines', 1.89), n=2)

    print('Subtotal: {}'.format(basket.subtotal()))
    print('Discount: {}'.format(basket.discount()))
    print('Total: {}'.format(basket.total()))

## What to do next

There are some parts that can be approved. For example, calculation of subtotal/discount can be cached. Also work with discounts can be slightly changed. At the moment discount is assigned to product, but it would be nice to be able to add several products to the same kind of discount.
