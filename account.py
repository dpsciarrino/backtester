
from orders import Order, _BUY, _SHORT, _MARKET, _STOP

class Account:
    def __init__(self, initial_balance=1000000.00):
        # Account Balance
        self._balance = initial_balance

        # Positions Variables
        self._maxPositions = 1          # Max number of positions
        self._inPosition = False        # Currently in a position
        self._numPositions = 0          # Number of positions currently in
    
    @property
    def balance(self):
        return self._balance
    
    @property
    def maxPositions(self):
        return self._maxPositions
    
    @property
    def numPositions(self):
        return self._numPositions
    
    @maxPositions.setter
    def maxPositions(self, n):
        if n <= 0:
            raise ValueError("Max Positions cannot be less than 1.")
        else:
            self._maxPositions = n

    def process_order(self, order:Order):
        '''
        process_order(order)

        Takes in an order, updates account balance, registers stop and limit values, etc.
        Returns the total cost of the order. If the order was a BUY order, the cost is
        negative. If the order is a sell order, the cost is positive.
        '''
        if order == None:
            return 0
        
        if self._maxPositions < 1:
            raise ValueError("Max Positions cannot be less than 1.")
        
        order_type = order.order_type
        order_direction = order.direction

        # Price x Shares = Total Order Amount
        order_price = float(order.price)
        order_shares = int(order.shares)
        order_total = order_price * order_shares

        
        # MARKET ORDERS
        #
        # If the order is a buy-at-market order, just buy at the given price.
        # If the order is a sell-at-market order, just sell at the given price.
        #
        if order_type == _MARKET:
            # If Max Positions is limited to 1 position at a time,
            # only sell if you previously bought and only buy if you
            # previously sold.
            if self._maxPositions == 1:
                if order_direction == _BUY:
                    if self._inPosition == False:
                        self._inPosition = True
                        self._balance = self._balance - order_total
                        return -1 * order_total
                elif order_direction == _SHORT:
                    if self._inPosition == True:
                        self._inPosition = False
                        self._balance = self._balance + order_total
                        return order_total
            
            # If Max Positions is limited by some finite number, then
            # buy or sell as you wish, within limits.
            elif self._maxPositions > 1:
                if order_direction == _BUY:
                    if self._numPositions < self._maxPositions:
                        self._numPositions += 1
                        self._inPosition = True
                        self._balance = self._balance - order_total
                        return -1 * order_total
                elif order_direction == _SHORT:
                    if self._numPositions != 0:
                        self._numPositions -= 1
                        if self._numPositions == 0:
                            self._inPosition = False
                        self._balance = self._balance + order_total
                        return order_total

        #
        # STOP LOSS ORDERS
        #
        # If the order is a stop loss order, make sure the price you want to stop loss at is
        # lower than the current price.
        elif order_type == _STOP:
            print("Stop Order not yet implemented")
            return 0


        return 0