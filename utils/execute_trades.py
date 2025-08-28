import numpy as np
import pandas as pd
from collections import deque
import matplotlib.pyplot as plt
from typing import List, Tuple, Deque

def execute_trades(
        inventory: Deque[Tuple[int,float]],
        mm_bid: float,
        mm_ask: float,
        bids: List[Tuple[float,int]],
        asks: List[Tuple[float,int]],
        trade_qty: int = 10,
        cost_per_share: float = 0.0) -> Tuple[Deque[Tuple[int,float]],float,List[Tuple[float,int]],List[Tuple[float,int]]]:
    # inventory is a queue of tuples of (price,qty) of blocks of shares bought at different prices
    # if qty > 0 (long position), if qty < 0 (short position)
    # mm_bid and mm_asks: bid and ask prices set by market maker
    # bids, asks: list of tupples (price,qty) representing market ask and bid books
    # trade_qty: 

    profit = 0

    # BUY LOGIC

    # allowed quantity to buy set by MM
    remaining_to_buy = trade_qty 

    while remaining_to_buy > 0 and asks and (mm_bid - asks[0][0] > cost_per_share):
        # get best avaialable ask price and qty
        ask_price, ask_qty = asks[0]
        # max number of stocks to potentially buy
        avail_qty_from_ask = min(remaining_to_buy,ask_qty)

        covered_short = 0

        # if we have short positions buy back those shares first
        if inventory and inventory[0][0] < 0:
            short_qty, short_price = inventory[0]
            covered_short = min(-short_qty,avail_qty_from_ask)
            avail_qty_from_ask -= covered_short         
            profit += covered_short * ( short_price - ask_price - cost_per_share )

            # remove short shares that we bought back from inventory
            if covered_short == -short_qty:
                inventory.popleft()
            else:
                inventory[0] = (short_qty+covered_short, short_price)

        # Add remaining shares to inventory
        if avail_qty_from_ask > 0:
            inventory.append((avail_qty_from_ask,ask_price))
            profit -= avail_qty_from_ask * cost_per_share

        total_traded = avail_qty_from_ask + covered_short

        # update stocks to buy
        remaining_to_buy -= total_traded

        # update asks book
        if total_traded == ask_qty:
            asks.pop(0)
        else:
            asks[0] = (ask_price, ask_qty - total_traded)


    # SELL LOGIC
    remaining_to_sell = trade_qty
    # run while mm wants to sell, there is inventory and market has bids at or above mm ask
    while remaining_to_sell > 0 and bids and (bids[0][0] - mm_ask > cost_per_share):
        
        # get best available bid price and qty
        bid_price, bid_qty = bids[0]
        avail_qty_from_bid = min(remaining_to_sell,bid_qty)

        # quantity still to sell after consuming long invnetory 
        qty_left_to_allocate = avail_qty_from_bid

        # Sell first from long inventory
        while qty_left_to_allocate > 0 and inventory and inventory[0][0]>0:
            inv_qty, inv_price = inventory[0]

            qty_sold = min(inv_qty,qty_left_to_allocate)
            profit += qty_sold * (bid_price - inv_price - cost_per_share)
            qty_left_to_allocate -= qty_sold

            # sell entire inventory block
            if qty_sold == inv_qty: 
                inventory.popleft()
            # partial sale
            else:
                inventory[0] = (inv_qty-qty_sold,inv_price)
        
        # If not enough long inventory short-sell
        if qty_left_to_allocate > 0:
            inventory.append((-qty_left_to_allocate,bid_price))
            profit -= qty_left_to_allocate * cost_per_share
            qty_left_to_allocate = 0
        
        remaining_to_sell -= avail_qty_from_bid

        # update bids book
        if avail_qty_from_bid == bid_qty:
            bids.pop(0)
        else:
            bids[0] = (bid_price, bid_qty-avail_qty_from_bid)
    
    return inventory, profit, bids, asks
