from datetime import datetime

# Order Directions
_BUY = 'buy'
_SELL = 'sell'
_SHORT = 'short'
_COVER = 'cover'

# Order Types
_MARKET = 'market'
_LIMIT = 'limit'
_STOP = 'stop'

class Order:
    '''
    Order

    Represents an Order in backtesting framework.
    '''
    def __init__(self, direction, order_type, shares:int, price:float, ticker:str=""): # ticker temporarily defaulted to ""

        if direction not in [_BUY, _SELL, _SHORT, _COVER]:
            raise ValueError('Direction must be valid direction value as specified in orders file.')

        if order_type not in [_MARKET, _LIMIT, _STOP]:
            raise ValueError('Order type must be market, limit, or stop')
        
        if type(shares) != int:
            raise TypeError('Shares must be int type.')
        
        if shares <= 0:
            raise ValueError('Shares must be positive')

        if type(price) != float:
            raise TypeError('Price must be float type.')

        if price <= 0.00:
            raise ValueError('Price must be a positive float value.')

        self._ticker = ticker
        self._direction = direction
        self._order_type = order_type
    
        self._shares = shares
        self._price = price

        self._submitted = None
        self._processed = None

    
    @property
    def ticker(self):
        return self._ticker

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
    
    @property
    def submitted(self):
        return self._submitted
    
    @property
    def processed(self):
        return self._processed
    
    @submitted.setter
    def submitted(self, t: datetime):
        self._submitted = t
    
    @processed.setter
    def processed(self, t: datetime):
        self._processed = t
    
    def order_dict(self):
        '''
        order_dict

        Returns a dictionary representation of the Order object.
        '''
        r = {}
        r['ticker'] = self._ticker
        r['order_type'] = self._order_type
        r['direction'] = self._direction
        r['shares'] = self._shares
        r['price'] = self._price
        r['submission_time'] = self._submitted

        return r
    
    def __str__(self):
        return "New Order" + "\n\tTicker: " + self.ticker +  "\n\tDirection: " + self.direction + "\n\tType: " + self.order_type + "\n\tShares: " + str(self.shares) + "\n\tPrice: $" + '{0:.2f}'.format(self.price) + "\n\tSubmitted: " + self.submitted.strftime('%m-%d-%y %H:%M:%S') 


def buy(order_type=_MARKET, shares=1, price=1.00, ticker=""):
    '''
    Creates a BUY Order object
    '''
    return Order(direction=_BUY, order_type=order_type, shares=shares, price=price, ticker=ticker)

def sell(order_type=_MARKET, shares=1, price=1.00, ticker=""):
    '''
    Creates a SELL Order object

    Meant to be used to sell an already-bought position
    '''
    return Order(direction=_SELL, order_type=order_type, shares=shares, price=price, ticker=ticker)

def short(order_type=_MARKET, shares=1, price=1.00, ticker=""):
    '''
    Creates a SHORT Order object
    '''
    return Order(direction=_SHORT, order_type=order_type, shares=shares, price=price, ticker=ticker)

def cover(order_type=_MARKET, shares=1, price=1.00, ticker=""):
    '''
    Creates an Order object meant to buy from a shorted position.
    '''
    return Order(direction=_COVER, order_type=order_type, shares=shares, price=price, ticker=ticker)