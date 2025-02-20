"""
Boilerplate Competitor Class
----------------------------

Instructions for Participants:
1. Do not import external libraries beyond what's provided.
2. Focus on implementing the `strategy()` method with your trading logic.
3. Use the provided methods to interact with the exchange:
   - self.create_limit_order(price, size, side, symbol) -> order_id if succesfully placed in order book or None
   - self.create_market_order(size, side, symbol) -> order_id if succesfully placed in order book or None
   - self.remove_order(order_id, symbol) -> bool
   - self.get_order_book_snapshot(symbol) -> dict
   - self.get_balance() -> float
   - self.get_portfolio() -> dict

   
Happy Trading!
"""

from typing import Optional, List, Dict

from Participant import Participant

class CompetitorBoilerplate(Participant):
    def __init__(self, 
                 participant_id: str,
                 order_book_manager=None,
                 order_queue_manager=None,
                 balance: float = 100000.0):
        """
        Initializes the competitor with default strategy parameters.
        
        :param participant_id: Unique ID for the competitor.
        :param order_book_manager: Reference to the OrderBookManager.
        :param order_queue_manager: Reference to the OrderQueueManager.
        :param balance: Starting balance for the competitor.
        """
        super().__init__(
            participant_id=participant_id,
            balance=balance,
            order_book_manager=order_book_manager,
            order_queue_manager=order_queue_manager
        )

        # Strategy parameters (fixed defaults)
        self.symbols: List[str] = ["NVR", "CPMD", "MFH", "ANG", "TVW"]
        
## ONLY EDIT THE CODE BELOW 

    def strategy(self):
        for symbol in self.symbols:
            # Cancel existing orders for this symbol
            for order_id in self.active_orders[symbol]['buy']:
                self.remove_order(order_id, symbol)
            for order_id in self.active_orders[symbol]['sell']:
                self.remove_order(order_id, symbol)
            self.active_orders = {symbol: {'buy': [], 'sell': []} for symbol in self.symbols}


            # Get the latest order book snapshot
            order_book = self.get_order_book_snapshot(symbol)
            if not order_book:
                continue  # Skip if no order book data is available

            # Extract best bid and ask prices
            best_bid = order_book['bids'][0][0] if order_book['bids'] else None
            best_ask = order_book['asks'][0][0] if order_book['asks'] else None

            if best_bid is None or best_ask is None:
                continue  # Skip if there's no market data

            # Calculate mid-price and current spread
            mid_price = (best_bid + best_ask) / 2
            current_spread = best_ask - best_bid

            # Dynamic spread adjustment (80% of current spread, minimum 0.01)
            desired_spread = max(current_spread * 0.8, 0.01)
            bid_price = round(mid_price - desired_spread / 2, 2)
            ask_price = round(mid_price + desired_spread / 2, 2)

            # Ensure bid and ask prices are within valid ranges
            bid_price = min(bid_price, best_ask - 0.01)  # Bid must be below best ask
            ask_price = max(ask_price, best_bid + 0.01)  # Ask must be above best bid

            # Position sizing based on available balance and current holdings
            cash_per_symbol = self.get_balance() / len(self.symbols)
            max_buy_size = int((cash_per_symbol * 0.1) // bid_price) if bid_price > 0 else 0
            current_holding = self.get_portfolio().get(symbol, 0)
            sell_size = max(int(current_holding * 0.1), 0)

            # Place buy order if conditions are met
            if max_buy_size > 0 and bid_price > 0:
                buy_order_id = self.create_limit_order(
                    price=bid_price,
                    size=max_buy_size,
                    side='buy',
                    symbol=symbol
                )
                if buy_order_id:
                    self.active_orders[symbol]['buy'].append(buy_order_id)

            # Place sell order if conditions are met
            if sell_size > 0 and ask_price > 0:
                sell_order_id = self.create_limit_order(
                    price=ask_price,
                    size=sell_size,
                    side='sell',
                    symbol=symbol
                )
                if sell_order_id:
                    self.active_orders[symbol]['sell'].append(sell_order_id)