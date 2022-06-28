import sys
import os
import pytest
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

######################
#  BASIC ORDER TESTS
######################

def test_negative_shares():
    with pytest.raises(ValueError):
        from orders import Order, _BUY, _MARKET
        order = Order(_BUY, _MARKET, -1, 10.00)

def test_zero_shares():
    with pytest.raises(ValueError):
        from orders import Order, _BUY, _MARKET
        order = Order(_BUY, _MARKET, 0, 10.00)

def test_float_shares():
    with pytest.raises(TypeError) as e_info:
        from orders import Order, _BUY, _MARKET
        order = Order(_BUY, _MARKET, 0.5, 10.00)

def test_integer_price():
    with pytest.raises(TypeError) as e_info:
        import orders as o
        order = o.Order(o._BUY, o._MARKET, 10, int(10), "SPY")

def test_order_direction():
    with pytest.raises(ValueError) as e_info:
        import orders as o
        order = o.Order('BuY', o._MARKET, 10, 10.00)

def test_order_type():
    with pytest.raises(ValueError) as e_info:
        import orders as o
        order = o.Order(o._BUY, 'marrket', 10, 54.93, "SPY")


@pytest.fixture
def basic_buy_order():
    import orders as o
    return o.Order(o._BUY, o._MARKET, 1, 10.00, "SPY")

def test_new_order_ticker(basic_buy_order):
    assert basic_buy_order.ticker == 'SPY'

def test_new_order_direction(basic_buy_order):
    assert basic_buy_order.direction == 'buy'

def test_new_order_ticker(basic_buy_order):
    assert basic_buy_order.order_type == 'market'

def test_new_order_shares(basic_buy_order):
    assert basic_buy_order.shares == 1

def test_new_order_price(basic_buy_order):
    assert basic_buy_order.price == 10.0

def test_processed_time_is_none(basic_buy_order):
    from datetime import datetime 
    d = datetime.now()
    basic_buy_order.submitted = d
    assert basic_buy_order.submitted == d
    assert basic_buy_order.processed == None

def test_new_order_dict(basic_buy_order):
    d = basic_buy_order.order_dict()
    assert d['ticker'] == 'SPY'
    assert d['order_type'] == 'market'
    assert d['direction'] == 'buy'
    assert d['shares'] == 1
    assert d['price'] == 10.0

######################
#   BUY ORDER TESTS
######################

@pytest.fixture
def create_buy_market_order():
    import orders as o
    order_type = o._MARKET
    shares = 10
    price = 7.05
    ticker="SPY"

    return o.buy(order_type=order_type, shares=shares, price=price, ticker=ticker)

@pytest.fixture
def create_sell_market_order():
    import orders as o
    order_type = o._MARKET
    shares = 10
    price = 8.01
    ticker="SPY"

    return o.sell(order_type=order_type, shares=shares, price=price, ticker=ticker)

@pytest.fixture
def create_short_market_order():
    import orders as o
    order_type = o._MARKET
    shares = 10
    price = 8.45
    ticker="SPY"

    return o.short(order_type=order_type, shares=shares, price=price, ticker=ticker)

@pytest.fixture
def create_cover_market_order():
    import orders as o
    order_type = o._MARKET
    shares = 10
    price = 8.45
    ticker="SPY"

    return o.cover(order_type, shares=shares, price=price, ticker=ticker)


def test_create_sell_market_order_direction(create_sell_market_order):
    assert create_sell_market_order.direction == 'sell'

def test_create_short_market_order_direction(create_short_market_order):
    assert create_short_market_order.direction == 'short'

def test_create_cover_market_order_direction(create_cover_market_order):
    assert create_cover_market_order.direction == 'cover'