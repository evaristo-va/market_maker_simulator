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
