from collections import deque
from typing import Deque, Tuple

def compute_unrealized_pnl(
	inventory: Deque[Tuple[int, float]], 
    current_price: float, 
    cost_per_share: float = 0.0
    ) -> float:
    
    pnl = 0

    for qty, price in inventory:
        if qty >=0:
            pnl += qty * (current_price-price-cost_per_share)
        else:
            pnl += -qty * (price-current_price-cost_per_share)

    return pnl
