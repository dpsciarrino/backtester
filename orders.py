# Order Types
_BUY = 'buy'
_SHORT = 'short'
_MARKET = 'market'
_LIMIT = 'limit'
_STOP = 'stop'

class Order:
    '''
    Order

    Represents an Order in backtesting framework.
    '''
    def __init__(self, direction, order_type, shares, price):
        self._direction = direction
        self._order_type = order_type
    
        self._shares = shares
        self._price = price
    
    @property
    def order_type(self):
        return self._order_type
    
    @property
    def direction(self):
        return self._direction
    
    @property
    def shares(self):
        return self._shares
    
    @property
    def price(self):
        return self._price
    
    def __str__(self):
        return "New Order" + "\n\tDirection: " + self.direction + "\n\tType: " + self.order_type + "\n\tShares: " + str(self.shares) + "\n\tPrice: " + str(self.price) + "\n"


def buy(order_type=_MARKET, shares=1, price=1.00):
    '''
    Creates a BUY Order object
    '''
    return Order(direction=_BUY, order_type=order_type, shares=shares, price=price)

def short(order_type=_MARKET, shares=1, price=1.00):
    '''
    Creates a SHORT/SELL Order object
    '''
    return Order(direction=_SHORT, order_type=order_type, shares=shares, price=price)

