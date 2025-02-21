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
            print(f"Processing {symbol}")

            # Get the latest order book snapshot
            order_book = self.get_order_book_snapshot(symbol)
            if not order_book:
                print(f"No order book data for {symbol}, skipping.")
                continue  # Skip if no order book data is available

            # Extract best bid and ask prices
            best_bid = order_book['bids'][0][0] if order_book['bids'] else None
            best_ask = order_book['asks'][0][0] if order_book['asks'] else None

            if best_bid is None or best_ask is None:
                print(f"No valid bid/ask for {symbol}, skipping.")
                continue  # Skip if there's no market data

            print(f"Best bid: {best_bid}, Best ask: {best_ask} for {symbol}")

            # Calculate mid-price and spread
            mid_price = (best_bid + best_ask) / 2
            spread = best_ask - best_bid

            # Fixed order size for consistency
            order_size = 20  # Restore fixed order size to ensure trades

            # Adjust bid/ask pricing for optimal execution
            bid_price = round(best_bid * 0.99, 2)
            ask_price = round(best_ask * 1.01, 2)

            print(f"Calculated bid: {bid_price}, ask: {ask_price} for {symbol}")
            print(f"Order size: {order_size}")

            # Place multiple buy and sell orders to smooth execution and maximize Sharpe ratio
            for i in range(4):  # Slightly increased trade frequency
                adjusted_bid = round(bid_price * (1 - 0.0007 * i), 2)
                adjusted_ask = round(ask_price * (1 + 0.0007 * i), 2)

                if adjusted_bid < best_ask:
                    buy_order_id = self.create_limit_order(
                        price=adjusted_bid,
                        size=order_size,
                        side='buy',
                        symbol=symbol
                    )
                    if buy_order_id:
                        print(f"Placed buy order {buy_order_id} at {adjusted_bid} for {symbol}")
                    else:
                        print(f"Buy order failed for {symbol}")

                if adjusted_ask > best_bid:
                    sell_order_id = self.create_limit_order(
                        price=adjusted_ask,
                        size=order_size,
                        side='sell',
                        symbol=symbol
                    )
                    if sell_order_id:
                        print(f"Placed sell order {sell_order_id} at {adjusted_ask} for {symbol}")
                    else:
                        print(f"Sell order failed for {symbol}")

