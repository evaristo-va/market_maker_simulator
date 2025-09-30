import numpy as np
from typing import Tuple


def get_bid_ask(
	price: float, 
    inventory_qty: int,
    sigma: int = 0.001, 
    market_spread: float = 0.05,    
    inventory_factor: float = 10
    ) -> Tuple[float, float]:

    # Generate market bid and ask prices each time
    alpha = (inventory_factor/100) * sigma * price
    
    bid = price - market_spread/2 - alpha * inventory_qty
    ask = price + market_spread/2 - alpha * inventory_qty 

    bid += np.random.uniform(0, market_spread/4)  # sometimes above best ask
    ask -= np.random.uniform(0, market_spread/4)  # sometimes below best bid

    return bid, ask


def get_bid_ask_avellaneda(
    price: float, 
    inventory_qty: int,
    tau: float,
    sigma: float = 0.001, # volatility parameter
    gamma: float = 0.0001, # risk aversion parameter
    k: float = 20 # order sensitivty parameter
    ) -> Tuple[float, float]:

    rtf = 1 - tau

    reservation_price = price - gamma * inventory_qty * sigma ** 2 * rtf

    optimal_half_spread = 0.5 * gamma * sigma ** 2 * rtf + (1/gamma) * np.log(1 + gamma/k)

    bid = reservation_price - optimal_half_spread
    ask = reservation_price + optimal_half_spread
       
    return bid, ask


