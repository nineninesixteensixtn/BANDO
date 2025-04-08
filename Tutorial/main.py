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
        # for product in state.order_depths:
        #     order_depth: OrderDepth = state.order_depths[product]
        #     orders: List[Order] = []
        #     acceptable_price = 10  # Participant should calculate this value
        #     print("Acceptable price : " + str(acceptable_price))
        #     print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(len(order_depth.sell_orders)))
    
        #     if len(order_depth.sell_orders) != 0:
        #         best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
        #         if int(best_ask) < acceptable_price:
        #             print("BUY", str(-best_ask_amount) + "x", best_ask)
        #             orders.append(Order(product, best_ask, -best_ask_amount))
    
        #     if len(order_depth.buy_orders) != 0:
        #         best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
        #         if int(best_bid) > acceptable_price:
        #             print("SELL", str(best_bid_amount) + "x", best_bid)
        #             orders.append(Order(product, best_bid, -best_bid_amount))
            
        # RESIN
        order_depth = state.order_depths['RAINFOREST_RESIN']
        orders = []
        min_bid = 9998
        max_ask = 10001

        if len(order_depth.sell_orders) > 0:
            best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
            if int(best_ask) < max_ask:
                print("BUY", str(-best_ask_amount) + "x", best_ask)
                orders.append(Order('RAINFOREST_RESIN', best_ask, -best_ask_amount))
            result['RAINFOREST_RESIN'] = orders

        if len(order_depth.buy_orders) > 0:
            best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
            if int(best_bid) > min_bid:
                print("BUY", str(-best_bid_amount) + "x", best_bid)
                orders.append(Order('RAINFOREST_RESIN', best_bid, -best_bid_amount))
            result['RAINFOREST_RESIN'] = orders

		    # String value holding Trader state data required. 
				# It will be delivered as TradingState.traderData on next execution.
        traderData = "SAMPLE" 
        
				# Sample conversion request. Check more details below. 
        conversions = 1
        return result, conversions, traderData

        
