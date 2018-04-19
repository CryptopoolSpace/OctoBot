import logging

from config.cst import CONFIG_ENABLED_OPTION
from trading.trader.order_manager import OrderManager
from trading.trader.portfolio import Portfolio
from trading.trader.trade import Trade


class Trader:
    def __init__(self, config, exchange):
        self.exchange = exchange
        self.config = config
        self.risk = self.config["trader"]["risk"]
        self.logger = logging.getLogger(self.__class__.__name__)
        self.simulate = False

        self.trades = []

        self.portfolio = Portfolio(self.config, self)

        self.order_manager = OrderManager(config, self)
        self.order_manager.start()

        # Debug
        if self.enabled():
            self.logger.debug("Enabled on " + self.exchange.get_name())
        else:
            self.logger.debug("Disabled on " + self.exchange.get_name())

    def enabled(self):
        if self.config["trader"][CONFIG_ENABLED_OPTION]:
            return True
        else:
            return False

    def get_risk(self):
        return self.risk

    def get_exchange(self):
        return self.exchange

    def get_portfolio(self):
        return self.portfolio

    def create_order(self, order_type, symbol, quantity, price=None, stop_price=None):
        # update_portfolio_available
        #
        # if linked_to is not None:
        #     linked_to.add_linked_order(order)
        #     order.add_linked_order(linked_to)

        pass

    def notify_order_cancel(self, order):
        # update portfolio with ended order
        self.portfolio.update_portfolio_available(order, False)

    def notify_order_close(self, order):
        # Cancel linked orders
        for linked_order in order.get_linked_orders():
            linked_order.cancel_order()
            self.order_manager.remove_order_from_list(linked_order)

        # update portfolio with ended order
        self.portfolio.update_portfolio(order)

        # add to trade history
        self.trades.append(Trade(self.exchange, order))

        # remove order to open_orders
        self.order_manager.remove_order_from_list(order)

    def get_open_orders(self):
        return self.order_manager.get_open_orders()

    def close_open_orders(self):
        pass

    def update_open_orders(self):
        # see exchange
        # -> update order manager
        pass

    def get_order_manager(self):
        return self.order_manager

    def stop_order_manager(self):
        self.order_manager.stop()

    def join_order_listeners(self):
        self.order_manager.join()