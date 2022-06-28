from datetime import datetime
from orders import Order, _BUY, _SHORT, _MARKET, _STOP

class Account:
    def __init__(self, initial_balance=1000000.00):
        # Account Balance
        self._balance = initial_balance

        # Positions Variables
        self._maxPositions = 1          # Max number of allowable positions
        self._inPosition = False        # Currently in a position
        self._numPositions = 0          # Number of positions currently in

        self._submission_order_list = {}

        self._executed_orders_list = []
    
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
    
    @property
    def submission_order_list(self):
        return self._submission_order_list
    
    @property
    def executed_orders_list(self):
        return self._executed_orders_list
    

    
    def submit_order(self, order:Order, submission_time:datetime=None, hasSubmissionTime:bool=True):
        '''
        submit_order

        All orders are added to an internal order submission list.
        '''

        if submission_time is not None and type(submission_time) != datetime:
            raise ValueError('Submission time must be of type datetime.')

        # Fill in the required order submission time
        if submission_time is None:
            submission_time = datetime.now()

        order.submitted = submission_time

        # Register the submitted order into the submission order list
        self._submission_order_list[len(self._submission_order_list)] = order

    
    def execute_order(self, order:Order) -> dict:
        '''
        Executes the next Order in the Order Submission list.

        - Returns a dict object representing the executed order.
        '''

        if order == None:
            raise ValueError('None-type passed as Order.')

        if len(self._submission_order_list) == 0:
            return None

        # Get most current order
        order_to_execute = self._submission_order_list[0]

        '''
        Account balance calculation is based on order type and order direction.
        '''
        # execute order account balance calculation
        

        # Add executed order to executed orders list
        self._executed_orders_list.append(order)






    def process_order(self, order:Order):
        '''
        process_order(order)

        Takes in an order, updates account balance, registers stop and limit values, etc.
        Returns the total cost of the order. If the order was a BUY order, the cost is
        negative. If the order is a sell order, the cost is positive.
        '''

        if order == None:
            return 0
        
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

        return 0