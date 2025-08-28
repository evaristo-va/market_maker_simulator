# Market-Making Simulation

This repository contains a Python simulation of a **market-making strategy** in a high-frequency trading environment. The project models intraday stock price dynamics, order book activity from market participants, and a market maker's bid-ask strategy. Both simple heuristic and Avellaneda-Stoikov optimal market-making strategies are implemented.

---

## Features

- **Geometric Brownian Motion (GBM) Price Simulation** : Simulates high-frequency stock prices with drift and volatility:

  $S_{t+\Delta t} = S_t \exp\Big[\big(\mu - \tfrac{1}{2}\sigma^2\big)\Delta t + \sigma \sqrt{\Delta t}\, Z\Big], \quad Z \sim \mathcal{N}(0,1)$
  
  - $\mu$: expected return rate per unit time  
  - $\sigma$: volatility per unit time  
  - $\Delta t$: time step of simulation  

- **Order Book Simulation**  
  Simulates stochastic bid and ask prices from other market participants:
  
  $P_{bid,i} = P_{ref}-U_i\cdot S +\epsilon_i, \quad$
  
  $P_{ask,i} = P_{ref}+U_i\cdot S - \epsilon_i$
  - $S$: maximum spread from reference price  
  - $U_i \sim \mathrm{Uniform}(0,1)$  
  - $\epsilon_i \sim \mathcal{N}(0,\sigma^2)$  
  - Bid and ask order arrivals follow Poisson processes  

- **Market Maker Bid-Ask Strategy**  
  Simple heuristic:
  
  $\text{Bid} = \bar{P} - \frac{S}{2} - I_F, \quad \text{Ask} = \bar{P} + \frac{S}{2} + I_F$
  
  - $I_F$: inventory factor to reduce risk from large positions  
  - If inventory is positive, reduce bid/ask to sell more and buy less  
  - If inventory is negative, increase bid/ask to buy back shares  

- **Trade Execution Logic**  
  - Buy if `MM_Bid - Market_Ask > cost_per_share`  
  - Sell if `Market_Bid - MM_Ask > cost_per_share`  
  - FIFO accounting for inventory: cover shorts first, then add to long inventory  
  - Allows short-selling if inventory is insufficient  

- **Profit and Loss Calculation**  
  - Realized P&L from executed trades  
  - Mark-to-market (MTM) P&L including unrealized positions  

---
