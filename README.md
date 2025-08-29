# Market-Making Simulation

This repository contains a Python simulation of a **market-making strategy** in a high-frequency trading environment. The project models intraday stock price dynamics, order book activity from market participants, and a market maker's bid-ask strategy. 

<p align="center">
  <img src="https://github.com/user-attachments/assets/543c475e-4c52-450a-8821-5beac7b2623d" alt="sm_image" width="586" height="387">
</p>

---

## Features

- **Geometric Brownian Motion (GBM) Price Simulation** : Simulates high-frequency stock prices with drift and volatility:
$S_{t+\Delta t} = S_t \exp\Big[\big(\mu - \tfrac{1}{2}\sigma^2\big)\Delta t + \sigma \sqrt{\Delta t}\, Z\Big], \quad Z \sim \mathcal{N}(0,1)$


  - $\mu$: expected return rate per unit time  
  - $\sigma$: volatility per unit time  
  - $\Delta t$: time step of simulation

  The actuall volatility of the one-step return is

  $\sigma_t=std \left(Log\left[\frac{S_t}{S_{t-1}}\right]\right)=\sigma\sqrt{\Delta t}$

- **Order Book Simulation**  
  Simulates stochastic bid and ask prices from other market participants:
  
  $P_{bid,i} = P_{ref}-U_i\cdot S +\epsilon_i\quad i=1,...,n_{bids}\quad; \quad \epsilon_i \sim \mathcal{N}(0,\sigma^2)\quad U_i\sim\mathrm{Uniform}(0,1)$
  
  $P_{ask,i} = P_{ref}+U_i\cdot S - \epsilon_i\quad i=1,...,n_{bids}\quad; \quad \epsilon_i \sim \mathcal{N}(0,\sigma^2)\quad U_i\sim\mathrm{Uniform}(0,1).$

  $n_{bids}\sim\mathrm{Poisson}(\lambda_{bid}\cdot\Delta t)\quad\quad n_{asks}\sim\mathrm{Poisson}(\lambda_{ask}\cdot\Delta t)$

  $P_{bid}=max(P_{bid,i})\quad\quad P_{ask}=min(P_{ask,i})\quad\quad\bar{P}=\frac{P_{bid}+P_{ask}}{2}$
  
  - $S$: spread range, maximum distance from the stock price for market participants to set buy and sell orders in the simulation.
  - $\lambda_{bid}, \lambda_{ask}$: order intensities, expected bid and ask order arrivals per unit time
  - $\sigma$: volatility, spread of noise term to allow ask prices to go below reference and asks above. Set as a percentage of reference price in the simulation

- **Market Maker Bid-Ask Strategy**  
  Simple heuristic:
  
  $\text{Bid} = \bar{P} - \frac{S}{2} - q\cdot\alpha_I(\sigma), \quad \text{Ask} = \bar{P} + \frac{S}{2} + q\cdot\alpha_I(\sigma) $
  with
  
  $\alpha_I(\sigma)=\frac{IF}{100}\cdot\sigma\cdot P $
  
  - $q$: number of shares on inventory
  - $\alpha_I$: inventory factor to reduce risk from holding large positions
  - $\sigma$: market volatility
  - $IF$: percentage change per unit volatility and inventory
    
If inventory is positive ($q>0$), reduce bid/ask to sell more and buy less. If inventory is negative ($q<0), increase bid/ask to buy back shares. The larger the volatility in the asset price the larger shift in the spread we should make.

The volatility in the asset price can be estimated using an exponential weigthed moving average

$\sigma_t^2 = \lambda\cdot\sigma_{t-1}^2 + (1-\lambda)\cdot r_{t-1}^2 $

- **Trade Execution Logic**  
  - Buy if `MM_Bid - Market_Ask > cost_per_share`  
  - Sell if `Market_Bid - MM_Ask > cost_per_share`  
  - FIFO accounting for inventory: cover shorts first, then add to long inventory  
  - Allows short-selling if inventory is insufficient  

- **Profit and Loss Calculation**  
  - Realized P&L from executed trades  
  - Mark-to-market (MTM) P&L including unrealized positions  

---
