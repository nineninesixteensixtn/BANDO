import json
from datamodel import Listing, Observation, Order, OrderDepth, ProsperityEncoder, Symbol, Trade, TradingState, Position
from typing import Any, List


# calculate quantity to order based on price

import json
from typing import Any

from datamodel import Listing, Observation, Order, OrderDepth, ProsperityEncoder, Symbol, Trade, TradingState


class Logger:
    def __init__(self) -> None:
        self.logs = ""
        self.max_log_length = 3750

    def print(self, *objects: Any, sep: str = " ", end: str = "\n") -> None:
        self.logs += sep.join(map(str, objects)) + end

    def flush(self, state: TradingState, orders: dict[Symbol, list[Order]], conversions: int, trader_data: str) -> None:
        base_length = len(
            self.to_json(
                [
                    self.compress_state(state, ""),
                    self.compress_orders(orders),
                    conversions,
                    "",
                    "",
                ]
            )
        )

        # We truncate state.traderData, trader_data, and self.logs to the same max. length to fit the log limit
        max_item_length = (self.max_log_length - base_length) // 3

        print(
            self.to_json(
                [
                    self.compress_state(state, self.truncate(state.traderData, max_item_length)),
                    self.compress_orders(orders),
                    conversions,
                    self.truncate(trader_data, max_item_length),
                    self.truncate(self.logs, max_item_length),
                ]
            )
        )

        self.logs = ""

    def compress_state(self, state: TradingState, trader_data: str) -> list[Any]:
        return [
            state.timestamp,
            trader_data,
            self.compress_listings(state.listings),
            self.compress_order_depths(state.order_depths),
            self.compress_trades(state.own_trades),
            self.compress_trades(state.market_trades),
            state.position,
            self.compress_observations(state.observations),
        ]

    def compress_listings(self, listings: dict[Symbol, Listing]) -> list[list[Any]]:
        compressed = []
        for listing in listings.values():
            compressed.append([listing.symbol, listing.product, listing.denomination])

        return compressed

    def compress_order_depths(self, order_depths: dict[Symbol, OrderDepth]) -> dict[Symbol, list[Any]]:
        compressed = {}
        for symbol, order_depth in order_depths.items():
            compressed[symbol] = [order_depth.buy_orders, order_depth.sell_orders]

        return compressed

    def compress_trades(self, trades: dict[Symbol, list[Trade]]) -> list[list[Any]]:
        compressed = []
        for arr in trades.values():
            for trade in arr:
                compressed.append(
                    [
                        trade.symbol,
                        trade.price,
                        trade.quantity,
                        trade.buyer,
                        trade.seller,
                        trade.timestamp,
                    ]
                )

        return compressed

    def compress_observations(self, observations: Observation) -> list[Any]:
        conversion_observations = {}
        for product, observation in observations.conversionObservations.items():
            conversion_observations[product] = [
                observation.bidPrice,
                observation.askPrice,
                observation.transportFees,
                observation.exportTariff,
                observation.importTariff,
                observation.sugarPrice,
                observation.sunlightIndex,
            ]

        return [observations.plainValueObservations, conversion_observations]

    def compress_orders(self, orders: dict[Symbol, list[Order]]) -> list[list[Any]]:
        compressed = []
        for arr in orders.values():
            for order in arr:
                compressed.append([order.symbol, order.price, order.quantity])

        return compressed

    def to_json(self, value: Any) -> str:
        return json.dumps(value, cls=ProsperityEncoder, separators=(",", ":"))

    def truncate(self, value: str, max_length: int) -> str:
        if len(value) <= max_length:
            return value

        return value[: max_length - 3] + "..."


logger = Logger()


        

class Trader:    

    AMETHYSTS = 'RAINFOREST_RESIN'
    STARFRUIT = 'KELP'
    SQUID = 'SQUID_INK'

    mid_price_ame = 10000

    limit_1_ame = 0
    mid_condition_ame = 20

    limit_0_star = -25
    limit_1_star = -20
    mid_condition_star = 20
    
    def quantity_buy_ame(self, position, price): 
       
        return 50 - position

    def quantity_sell_ame(self, position, price): 
   
        return -50 - position 
    
    def quantity_buy(self, position): 
        return 50 - position

    def quantity_sell(self, position): 
        return -50 - position 


    def price_buy_star(self, price, amount, position, mid_price): 
        profit = abs(mid_price - price)
        if profit == 0.5:
            return price - 1
        
        elif profit == 1 and position > self.limit_0_star:
            return price
        
        elif abs(amount) == 1 and profit == 1.5: 
            return price
        
        elif profit == 1.5 and position > self.limit_1_star: 
            return price
        
        
        return price + 1 


    def price_sell_star(self, price, amount, position, mid_price): 
        profit = abs(mid_price - price)
        if profit == 0.5:
            return price + 1
        
        elif profit == 1 and position < -self.limit_0_star:
            return price

        elif abs(amount) == 1 and profit == 1.5:
            return price
        
        elif profit == 1.5 and position < -self.limit_1_star: 
            return price
        
        
        return price - 1
    

    def sell_star(self, product, best_bid, best_bid_amount, best_bid2, best_bid_amount2, best_ask, best_ask_amount, best_ask2, best_ask_amount2, best_ask3, best_ask_amount3, position, mid_price): 
        no_exceed = 0
        orders = []
        # Market take if price is higher than 10,000
        if int(best_bid) > mid_price:
            if abs(mid_price - best_bid) != 0.5 or position > self.mid_condition_star:
                orders.append(Order(product, best_bid, -best_bid_amount))
                no_exceed = best_bid_amount 

            
            if int(best_bid2) > mid_price and (abs(mid_price - best_bid2) != 0.5 or position > self.mid_condition_star):
                orders.append(Order(product, best_bid2, max(-best_bid_amount2, -position + no_exceed + 2)))
                no_exceed += max(-best_bid_amount2, -position + no_exceed + 2)
            
            orders.append(Order(product, self.price_sell_star(best_ask, best_ask_amount, position, mid_price), self.quantity_sell(position) + no_exceed))

        elif int(best_bid) == mid_price and position > 5: 
            orders.append(Order(product, best_bid, max(-best_bid_amount2, -position + no_exceed + 2)))
            no_exceed = max(-best_bid_amount2, -position + no_exceed + 2)

            orders.append(Order(product, self.price_sell_star(best_ask, best_ask_amount, position, mid_price), self.quantity_sell(position)))


        elif int(best_ask) > mid_price: 
            orders.append(Order(product, self.price_sell_star(best_ask, best_ask_amount, position, mid_price), self.quantity_sell(position)))

        if best_ask2 != 0:
            if int(best_ask) < mid_price and int(best_ask2) < mid_price: 
                orders.append(Order(product, self.price_sell_star(best_ask3, best_ask_amount3, position, mid_price), self.quantity_sell(position)))
            
            elif int(best_ask) < mid_price: 
                orders.append(Order(product, self.price_sell_star(best_ask2, best_ask_amount2, position, mid_price), self.quantity_sell(position)))
        return orders

    def buy_star(self, product, best_bid, best_bid_amount, best_bid2, best_bid_amount2, best_bid3, best_bid_amount3, best_ask, best_ask_amount, best_ask2, best_ask_amount2, position, mid_price): 
        no_exceed = 0
        orders = []
        # Buy when the price is less than 10,000
        if int(best_ask) < mid_price:
            if abs(mid_price - best_ask) != 0.5 or position < -self.mid_condition_star:
                orders.append(Order(product, best_ask, -best_ask_amount))
                no_exceed = best_ask_amount
            
            if int(best_ask2) < mid_price and (abs(mid_price - best_ask2) != 0.5 or position < -self.mid_condition_star): 
                orders.append(Order(product, best_ask2, min(-best_ask_amount2, -position - no_exceed -2)))
                no_exceed += min(-best_ask_amount2, -position - no_exceed -2)
        
            orders.append(Order(product, self.price_buy_star(best_bid, best_bid_amount, position, mid_price), self.quantity_buy(position) + no_exceed))

        elif int(best_ask) == mid_price and position < -5: 
            orders.append(Order(product, best_ask, min(-best_ask_amount2, -position - no_exceed -2)))
            no_exceed = min(-best_ask_amount2, -position - no_exceed-2)
        
            orders.append(Order(product, self.price_buy_star(best_bid, best_bid_amount, position, mid_price), self.quantity_buy(position)))

        elif int(best_bid) < mid_price: 
            orders.append(Order(product, self.price_buy_star(best_bid, best_bid_amount, position, mid_price), self.quantity_buy(position)))
               
        if best_bid2 != 0:
            if int(best_bid) > mid_price and int(best_bid2) > mid_price: 
                orders.append(Order(product, self.price_buy_star(best_bid3, best_bid_amount3, position, mid_price), self.quantity_buy(position)))

            elif int(best_bid) > mid_price: 
                orders.append(Order(product, self.price_buy_star(best_bid2, best_bid_amount2, position, mid_price), self.quantity_buy(position)))
        
        return orders

    # Limit market making at $1 profit if high inventory
    # Market make at bid_price if bid_amount is 1.
    def price_buy_ame(self, price, amount, position): 
        profit = abs(self.mid_price_ame - price)

        if profit == 2 and position >= self.limit_1_ame:
            return price 
        
        return price + 1 

    # Limit market making at $1 profit if high short inventory
    # Market make at bid_price if bid_amount is 1.
    def price_sell_ame(self, price, amount, position): 
        profit = abs(self.mid_price_ame - price)
        
        if profit == 2 and position <= -self.limit_1_ame: 
            return price
     
        return price - 1
    
    def buy_ame(self, product, best_bid, best_bid_amount, best_bid2, best_bid_amount2, best_bid3, best_bid_amount3, best_ask, best_ask_amount, best_ask2, best_ask_amount2, best_ask3, best_ask_amount3, position): 
        no_exceed = 0
        orders = []
        # Buy when the price is less than 10,000
        mid_price = self.mid_price_ame
            

        if int(best_ask) < mid_price:
            orders.append(Order(product, best_ask, -best_ask_amount))
            no_exceed = best_ask_amount

            # If Market taking then market make at a price from highest bid.
            # e.g position: -4 buy 6   so 2 , -3
            if best_ask2 == 10000 and position < -self.mid_condition_ame and -position - no_exceed > 0:
                orders.append(Order(product, 10000, min(-best_ask_amount2, -position - no_exceed)))
                no_exceed += -min(-best_ask_amount2, -position - no_exceed)

            orders.append(Order(product, self.price_buy_ame(best_bid, best_bid_amount, position), self.quantity_buy_ame(position, best_bid) + no_exceed))


        # If the pr

        elif int(best_ask) == mid_price and position < -self.mid_condition_ame: 
            orders.append(Order(product, 10000, min(-best_ask_amount, -position)))

            no_exceed = -min(-best_ask_amount, -position)

            orders.append(Order(product, self.price_buy_ame(best_bid, best_bid_amount, position), self.quantity_buy_ame(position, best_bid) + no_exceed))

        # If the prices are less then the bid then market make with higest bi


        elif int(best_bid) < mid_price: 
            orders.append(Order(product, self.price_buy_ame(best_bid, best_bid_amount, position), self.quantity_buy_ame(position, best_bid)))

        # if the price is higher than the bid than market make with second highest bid

        elif best_bid2 != 0:
            if int(best_bid2) >= mid_price:
                orders.append(Order(product, self.price_buy_ame(best_bid3, best_bid_amount3, position), self.quantity_buy_ame(position, best_bid3)))

            elif int(best_bid) >= mid_price:
                orders.append(Order(product, self.price_buy_ame(best_bid2, best_bid_amount2, position), self.quantity_buy_ame(position, best_bid2)))
            
        return orders
 

    def sell_ame(self, product, best_bid, best_bid_amount, best_bid2, best_bid_amount2, best_bid3, best_bid_amount3, best_ask, best_ask_amount, best_ask2, best_ask_amount2, best_ask3, best_ask_amount3, position):
        no_exceed = 0
        orders = []
        mid_price = self.mid_price_ame
        # Market take if price is higher than 10,000
        if int(best_bid) > mid_price:
            orders.append(Order(product, best_bid, -best_bid_amount))
            no_exceed = best_bid_amount

            # e.g position: 2, sell 4,  or sell -3

            if best_bid2 == 10000 and position > self.mid_condition_ame and -position + no_exceed < 0:
                orders.append(Order(product, 10000, max(-best_bid_amount2, -position + no_exceed)))
                no_exceed += -max(-best_bid_amount2, -position + no_exceed)

            # Market make at the 
            orders.append(Order(product, self.price_sell_ame(best_ask, best_ask_amount, position), self.quantity_sell_ame(position, best_ask) + no_exceed))

        elif int(best_bid) == mid_price and position > self.mid_condition_ame: 
            orders.append(Order(product, 10000, max(-best_bid_amount, -position)))
            no_exceed = -max(-best_bid_amount, -position)
          
            orders.append(Order(product, self.price_sell_ame(best_ask, best_ask_amount, position), self.quantity_sell_ame(position, best_ask) + no_exceed))

        # Market make with best_ask
        elif int(best_ask) > mid_price: 
            orders.append(Order(product, self.price_sell_ame(best_ask, best_ask_amount, position), self.quantity_sell_ame(position, best_ask)))

        # Market make with second best_ask
        elif int(best_ask2) != 0:
            if int(best_ask2) <= mid_price:
               orders.append(Order(product, self.price_sell_ame(best_ask3, best_ask_amount3, position), self.quantity_sell_ame(position, best_ask3)))

            elif int(best_ask) <= mid_price: 
                orders.append(Order(product, self.price_sell_ame(best_ask2, best_ask_amount2, position), self.quantity_sell_ame(position, best_ask2)))
            
        return orders

    def run(self, state: TradingState) -> tuple[dict[Symbol, list[Order]], int, str]:
        results = {}
        conversions = 0
        trader_data = ""

		# Orders to be placed on exchange matching engine
        for product in state.order_depths:

            order_depth: OrderDepth = state.order_depths[product]
            
            if product in state.position:
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

            worst_ask, worst_vol = list(order_depth.sell_orders.items())[-1]
            worst_bid, worst_bid_amount2 = list(order_depth.buy_orders.items())[-1] 
            
            mid_price = (worst_ask + worst_bid)/2
      



            if product == self.AMETHYSTS:
                results[product] = self.buy_ame(product, best_bid, best_bid_amount, best_bid2, best_bid_amount2, best_bid3, best_bid_amount3 ,best_ask, best_ask_amount, best_ask2, best_ask_amount2, best_ask3, best_ask_amount3, position) + self.sell_ame(product, best_bid, best_bid_amount, best_bid2, best_bid_amount2, best_bid3, best_bid_amount3, best_ask, best_ask_amount, best_ask2, best_ask_amount2, best_ask3, best_ask_amount3, position)
            elif product == self.STARFRUIT: 
                results[product] = self.sell_star(product, best_bid, best_bid_amount, best_bid2, best_bid_amount2, best_ask, best_ask_amount, best_ask2, best_ask_amount2, best_ask3, best_ask_amount3, position, mid_price) + self.buy_star(product, best_bid, best_bid_amount, best_bid2, best_bid_amount2, best_bid3, best_bid_amount3, best_ask, best_ask_amount, best_ask2, best_ask_amount2, position, mid_price)
            elif product == self.SQUID: 
                results[product] = self.sell_star(product, best_bid, best_bid_amount, best_bid2, best_bid_amount2, best_ask, best_ask_amount, best_ask2, best_ask_amount2, best_ask3, best_ask_amount3, position, mid_price) + self.buy_star(product, best_bid, best_bid_amount, best_bid2, best_bid_amount2, best_bid3, best_bid_amount3, best_ask, best_ask_amount, best_ask2, best_ask_amount2, position, mid_price)
        logger.flush(state, results, conversions, trader_data)
        return results, conversions, trader_data
