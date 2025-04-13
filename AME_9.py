import json
from datamodel import Listing, Observation, Order, OrderDepth, ProsperityEncoder, Symbol, Trade, TradingState, Position
from typing import Any, List




# class Logger:
#     def __init__(self) -> None:
#         self.logs = ""

#     def print(self, *objects: Any, sep: str = " ", end: str = "\n") -> None:
#         self.logs += sep.join(map(str, objects)) + end

#     def flush(self, state: TradingState, orders: dict[Symbol, list[Order]], conversions: int, trader_data: str) -> None:
#         print(json.dumps([
#             self.compress_state(state),
#             self.compress_orders(orders),
#             conversions,
#             trader_data,
#             self.logs,
#         ], cls=ProsperityEncoder, separators=(",", ":")))

#         self.logs = ""

#     def compress_state(self, state: TradingState) -> list[Any]:
#         return [
#             state.timestamp,
#             state.traderData,
#             self.compress_listings(state.listings),
#             self.compress_order_depths(state.order_depths),
#             self.compress_trades(state.own_trades),
#             self.compress_trades(state.market_trades),
#             state.position,
#             self.compress_observations(state.observations),
#         ]

#     def compress_listings(self, listings: dict[Symbol, Listing]) -> list[list[Any]]:
#         compressed = []
#         for listing in listings.values():
#             compressed.append([listing["symbol"], listing["product"], listing["denomination"]])

#         return compressed

#     def compress_order_depths(self, order_depths: dict[Symbol, OrderDepth]) -> dict[Symbol, list[Any]]:
#         compressed = {}
#         for symbol, order_depth in order_depths.items():
#             compressed[symbol] = [order_depth.buy_orders, order_depth.sell_orders]

#         return compressed

#     def compress_trades(self, trades: dict[Symbol, list[Trade]]) -> list[list[Any]]:
#         compressed = []
#         for arr in trades.values():
#             for trade in arr:
#                 compressed.append([
#                     trade.symbol,
#                     trade.price,
#                     trade.quantity,
#                     trade.buyer,
#                     trade.seller,
#                     trade.timestamp,
#                 ])

#         return compressed

#     def compress_observations(self, observations: Observation) -> list[Any]:
#         conversion_observations = {}
#         for product, observation in observations.conversionObservations.items():
#             conversion_observations[product] = [
#                 observation.bidPrice,
#                 observation.askPrice,
#                 observation.transportFees,
#                 observation.exportTariff,
#                 observation.importTariff,
#                 observation.sunlight,
#                 observation.humidity,
#             ]

#         return [observations.plainValueObservations, conversion_observations]

#     def compress_orders(self, orders: dict[Symbol, list[Order]]) -> list[list[Any]]:
#         compressed = []
#         for arr in orders.values():
#             for order in arr:
#                 compressed.append([order.symbol, order.price, order.quantity])

#         return compressed

# logger = Logger()


# calculate quantity to order based on price



class Trader:    

        
    AMETHYSTS = 'RAINFOREST_RESIN'
    STARFRUIT = 'KELP'

    mid_price = 10000
    limit_1 = 0
    mid_condition = 9
    MAX_POS = 50
    
    
    def quantity_buy(self, position, price): 
        if abs(self.mid_price - price) == 2 and position <= self.MAX_POS: 
            return self.MAX_POS - position
        elif abs(self.mid_price - price) == 2: 
            return 0
        
        return self.MAX_POS - position
    

    def quantity_sell(self, position, price): 

        if abs(self.mid_price - price) == 2 and position >= -self.MAX_POS:
            return -self.MAX_POS - position 
        elif abs(self.mid_price - price) == 2: 
            return 0
        
        return -self.MAX_POS - position
    

    # Limit market making at $1 profit if high inventory
    # Market make at bid_price if bid_amount is 1.
    def price_buy(self, price, amount, position): 
        profit = abs(self.mid_price - price)


        if profit == 2 and position >= self.limit_1:
            return price 
        
    
        
        return price + 1 

    # Limit market making at $1 profit if high short inventory
    # Market make at bid_price if bid_amount is 1.
    def price_sell(self, price, amount, position): 
        profit = abs(self.mid_price - price)
        
 
        if profit == 2 and position <= -self.limit_1: 
            return price
     
        return price -1
    
    def buy_ame(self, product, best_bid, best_bid_amount, best_bid2, best_bid_amount2, best_bid3, best_bid_amount3, best_ask, best_ask_amount, best_ask2, best_ask_amount2, best_ask3, best_ask_amount3, position, mid_price): 
        no_exceed = 0
        orders = []
        # Buy when the price is less than 10,000

            

        if int(best_ask) < mid_price:
            orders.append(Order(product, best_ask, -best_ask_amount))
            no_exceed = best_ask_amount

            # If Market taking then market make at a price from highest bid.
            if best_ask2 == 10000 and position < -self.mid_condition:
                orders.append(Order(product, 10000, min(-best_ask_amount2, -position)))
                no_exceed += -min(-best_ask_amount2, -position)

            orders.append(Order(product, self.price_buy(best_bid, best_bid_amount, position), self.quantity_buy(position, best_bid) + no_exceed))


        # If the pr

        elif int(best_ask) == mid_price and position < -self.mid_condition: 
            orders.append(Order(product, 10000, min(-best_ask_amount, -position)))

            no_exceed = -min(-best_ask_amount, -position)

            orders.append(Order(product, self.price_buy(best_bid, best_bid_amount, position), self.quantity_buy(position, best_bid) + no_exceed))

        # If the prices are less then the bid then market make with higest bi


        elif int(best_bid) < mid_price: 
            orders.append(Order(product, self.price_buy(best_bid, best_bid_amount, position), self.quantity_buy(position, best_bid)))

        # if the price is higher than the bid than market make with second highest bid

        elif best_bid2 != 0:
            if int(best_bid2) >= mid_price:
               orders.append(Order(product, self.price_buy(best_bid3, best_bid_amount3, position), self.quantity_buy(position, best_bid3)))

            elif int(best_bid) >= mid_price:
                orders.append(Order(product, self.price_buy(best_bid2, best_bid_amount2, position), self.quantity_buy(position, best_bid2)))
            
        return orders
 

    def sell_ame(self, product, best_bid, best_bid_amount, best_bid2, best_bid_amount2, best_bid3, best_bid_amount3, best_ask, best_ask_amount, best_ask2, best_ask_amount2, best_ask3, best_ask_amount3, position, mid_price):
        no_exceed = 0
        orders = []
        # Market take if price is higher than 10,000
        if int(best_bid) > mid_price:
            orders.append(Order(product, best_bid, -best_bid_amount))
            no_exceed = best_bid_amount

            if best_bid2 == 10000 and position > self.mid_condition:
                orders.append(Order(product, 10000, max(-best_bid_amount2, -position)))
                no_exceed += -max(-best_bid_amount2, -position)

            # Market make at the 
            orders.append(Order(product, self.price_sell(best_ask, best_ask_amount, position), self.quantity_sell(position, best_ask) + no_exceed))

        elif int(best_bid) == mid_price and position > self.mid_condition: 
            orders.append(Order(product, 10000, max(-best_bid_amount, -position)))
            no_exceed = -max(-best_bid_amount, -position)
          
            orders.append(Order(product, self.price_sell(best_ask, best_ask_amount, position), self.quantity_sell(position, best_ask) + no_exceed))

        # Market make with best_ask
        elif int(best_ask) > mid_price: 
            orders.append(Order(product, self.price_sell(best_ask, best_ask_amount, position), self.quantity_sell(position, best_ask)))

        # Market make with second best_ask
        elif int(best_ask2) != 0:
            if int(best_ask2) <= mid_price:
              orders.append(Order(product, self.price_sell(best_ask3, best_ask_amount3, position), self.quantity_sell(position, best_ask3)))

            elif int(best_ask) <= mid_price: 
                orders.append(Order(product, self.price_sell(best_ask2, best_ask_amount2, position), self.quantity_sell(position, best_ask2)))
            
        return orders

    def run(self, state: TradingState) -> tuple[dict[Symbol, list[Order]], int, str]:
        results = {}
        conversions = 0
        trader_data = ""

		# Orders to be placed on exchange matching engine

        mid_price = 10000
        product = self.AMETHYSTS
        order_depth: OrderDepth = state.order_depths[product]
        orders: List[Order] = []

        if len(state.position) != 0:
            position = int(state.position[product])
        else: 
            position = 0

        best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0] 
        best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]

        if len(order_depth.buy_orders) >= 2: 
            best_bid2, best_bid_amount2 = list(order_depth.buy_orders.items())[1] 
        else: 
            best_bid2 = 0
            best_bid_amount2 = 0

        if len(order_depth.sell_orders) >= 2: 
            best_ask2, best_ask_amount2 = list(order_depth.sell_orders.items())[1]
        else: 
            best_ask2 = 0
            best_ask_amount2 = 0

        if len(order_depth.buy_orders) >= 3: 
            best_bid3, best_bid_amount3 = list(order_depth.buy_orders.items())[2] 
        else: 
            best_bid3 = 0
            best_bid_amount3 = 0

        if len(order_depth.sell_orders) >= 3: 
            best_ask3, best_ask_amount3 = list(order_depth.sell_orders.items())[2]
        else: 
            best_ask3 = 0
            best_ask_amount3 = 0

        results[product] = self.buy_ame(product, best_bid, best_bid_amount, best_bid2, best_bid_amount2, best_bid3, best_bid_amount3 ,best_ask, best_ask_amount, best_ask2, best_ask_amount2, best_ask3, best_ask_amount3, position, mid_price) + self.sell_ame(product, best_bid, best_bid_amount, best_bid2, best_bid_amount2, best_bid3, best_bid_amount3, best_ask, best_ask_amount, best_ask2, best_ask_amount2, best_ask3, best_ask_amount3, position, mid_price)

        # logger.flush(state, results, conversions, trader_data)
        return results, conversions, trader_data