from datetime import timedelta
import sys
import os
import pytest

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

@pytest.fixture
def basic_account_fixture():
    from account import Account 
    return Account()

def test_initial_account_balance(basic_account_fixture):
    assert basic_account_fixture.balance == 1000000.00

def test_initial_maximum_allowable_positions(basic_account_fixture):
    assert basic_account_fixture.maxPositions == 1

def test_initial_number_of_open_positions(basic_account_fixture):
    assert basic_account_fixture.numPositions == 0

def test_max_positions_negative_value(basic_account_fixture):
    with pytest.raises(ValueError):
        basic_account_fixture.maxPositions = -1

def test_max_positions_changes(basic_account_fixture):
    basic_account_fixture.maxPositions = 5
    assert basic_account_fixture.maxPositions == 5

@pytest.fixture
def order_submission_fixture():
    from account import Account
    from datetime import datetime
    from orders import Order, _BUY, _SELL, _MARKET

    # Create Orders without submission times
    orders_without_submission_times = []
    o1_b = Order(_BUY, _MARKET, 1, 420.01, "TSLA")
    o1_s = Order(_SELL, _MARKET, 1, 450.10, "TLSA")
    o2_b1 = Order(_BUY, _MARKET, 1, 300.00, "TSLA")
    o2_b2 = Order(_BUY, _MARKET, 1, 350.01, "TSLA")
    o2_s = Order(_SELL, _MARKET, 2, 325.50, "TSLA")

    orders_without_submission_times.append(o1_b)
    orders_without_submission_times.append(o1_s)
    orders_without_submission_times.append(o2_b1)
    orders_without_submission_times.append(o2_b2)
    orders_without_submission_times.append(o2_s)

    # Create dates list for order submission
    dates = []
    dt = 0
    t = datetime.now()
    for i in range(0, len(orders_without_submission_times)):
        dates.append(t + timedelta(minutes=dt))
        dt += 5
    
    # Create account
    acnt = Account(initial_balance=1000.00)

    return acnt, orders_without_submission_times, dates

def test_adding_orders_to_account(order_submission_fixture):
    acnt = order_submission_fixture[0]
    orders_without_submission_times = order_submission_fixture[1]
    dates = order_submission_fixture[2]

    d = 0
    for order in orders_without_submission_times:
        acnt.submit_order(order, dates[d])
        d += 1

    assert len(acnt.submission_order_list) == d

def test_ordering_of_submitted_orders(order_submission_fixture):
    '''
    The submitted orders dict is maintained to have the earliest submitted order
    at index zero, and the latest submitted order at index N-1.
    '''
    acnt = order_submission_fixture[0]
    orders_without_submission_times = order_submission_fixture[1]
    dates = order_submission_fixture[2]

    d = 0
    for order in orders_without_submission_times:
        acnt.submit_order(order=order, submission_time=dates[d])
        d += 1
    
    submission_order_dict = acnt.submission_order_list
    
    last_order_time = None
    for k,v in submission_order_dict.items():
        current_order_time = v.submitted

        if last_order_time == None:
            last_order_time = current_order_time
            continue
            
        assert current_order_time >= last_order_time

def test_execute_order_list_appending(order_submission_fixture):
    from orders import Order
    acnt = order_submission_fixture[0]
    orders_without_submission_times = order_submission_fixture[1]
    dates = order_submission_fixture[2]

    first_executed: Order = None
    d = 0
    for order in orders_without_submission_times:
        if d == 0:
            first_executed = order
        acnt.submit_order(order=order, submission_time=dates[d])
        d += 1
    
    acnt.execute_order(first_executed)

    assert str(first_executed) == str(acnt.executed_orders_list[0])

    
