import numpy as np
from datamodel import OrderDepth, Order, TradingState
from typing import List, Dict

class StoikovTrader:
    def __init__(self, gamma=0.1, k=1.5):
        """
        Initializes the trader with market-making parameters.
        Now, all past prices and volatility values are hardcoded.
        """
        self.gamma = gamma  # Risk aversion parameter
        self.k = k  # Market depth parameter

        # Hardcoded inventory values (initialized to 0)
        self.inventory = {
            "RAINFOREST_RESIN": 0,
            "KELP": 0,
        }

        # Hardcoded past prices (from CSV)
        self.past_prices = {
            "RAINFOREST_RESIN": [10000.0, 9999.0, 10000.0, 10001.0, 10001.0, 10000.0, 10000.0, 10003.5, 9999.0],
            "KELP": [2028.5, 2026.5, 2026.5, 2026.5, 2026.5, 2026.5, 2027.0, 2026.5, 2025.5],
        }

        # Hardcoded volatility values
        self.volatility = {
            "RAINFOREST_RESIN": 2.1033805774993115,
            "KELP": 0.7792076184956056,
        }

    def compute_stoikov_prices(self, mid_price, inventory, sigma):
        """
        Compute reservation price and optimal spread using Stoikov model.
        """
        reservation_price = mid_price - (self.gamma * sigma**2 * inventory / self.k)
        optimal_spread = (1 / self.k) + (self.gamma * sigma**2)
        return reservation_price, optimal_spread

    def run(self, state: TradingState):
        """
        Main trading function: Processes market data and places trades.
        """
        result = {}
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []

            best_bid = max(order_depth.buy_orders.keys(), default=None)
            best_ask = min(order_depth.sell_orders.keys(), default=None)

            if best_bid is None or best_ask is None:
                continue 

            mid_price = (best_bid + best_ask) / 2

            if product not in self.inventory:
                self.inventory[product] = 0

            sigma = self.volatility.get(product, 0)

            reservation_price, optimal_spread = self.compute_stoikov_prices(
                mid_price, self.inventory[product], sigma
            )

            bid_price = reservation_price - optimal_spread / 2
            ask_price = reservation_price + optimal_spread / 2

            if bid_price > best_bid:
                orders.append(Order(product, int(bid_price), 10))

            if ask_price < best_ask:
                orders.append(Order(product, int(ask_price), -10))

            result[product] = orders

            traderData = "SAMPLE"
            conversions = 0

        return result, conversions, traderData

        
