import numpy as np
from typing import Tuple


def get_bid_ask(
	price: float, 
    inventory_qty: int, 
    market_spread: float = 0.05,    
    inventory_factor: float = 0.01
    ) -> Tuple[float, float]:

    # Generate market bid and ask prices each time
    adj = (inventory_qty/100) * inventory_factor * price
    bid = price - market_spread/2 - adj 
    ask = price + market_spread/2 - adj 

    bid += np.random.uniform(0, market_spread/4)  # sometimes above best ask
    ask -= np.random.uniform(0, market_spread/4)  # sometimes below best bid

    return bid, ask
