from ..Constants.constants import Stock_Action


class Stock_Performance_Result:

    def __init__(self):
        self.stock_action = None
        self.actual_delta = 0.0

    def attach_profit_sell_action(self, actual_delta: float):
        self.actual_delta = actual_delta
        self.stock_action = Stock_Action.PROFIT_SELL

    def attach_loss_sell_action(self, actual_delta: float):
        self.actual_delta = actual_delta
        self.stock_action = Stock_Action.LOSS_SELL