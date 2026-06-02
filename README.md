# Trader Performance vs Bitcoin Market Sentiment
### Hyperliquid × Fear & Greed Index — Data Science Analysis

---

## Overview

This project explores whether **Bitcoin market sentiment** — measured by the daily
Fear & Greed Index (FGI) — has a statistically meaningful impact on trader profitability
on the **Hyperliquid** decentralised derivatives exchange.

The core hypothesis: *in a market driven by crowd psychology rather than fundamentals,
sentiment is not just noise — it is signal. Traders who align their directional bias
with the FGI should outperform those who ignore it.*

This was submitted as part of the **Primetrade.ai Data Science Internship Assignment**.

---

## Key Findings at a Glance

| Sentiment | Avg PnL / Trade | Win Rate | Best Side |
|-----------|----------------|----------|-----------|
| Extreme Fear | $34.54 | ~37% | SELL marginally |
| **Fear** | **$54.29** | **~43%** | **BUY strongly** |
| Neutral | $34.31 | ~40% | SELL marginally |
| Greed | $42.74 | ~39% | SELL strongly |
| Extreme Greed | $67.89 | ~44% | **SELL strongly ($114.58)** |

**Top insight:** SELL trades in Extreme Greed average **$114.58** — nearly **11x** more
than BUY trades ($10.50) in the same regime. Shorting into euphoria is the single
most profitable strategy in this dataset.

---

## Dataset

| File | Description |
|------|-------------|
| `historical_data.csv` | 211,218 individual trades from 32 Hyperliquid wallets |
| `fear_greed_index.csv` | Daily Bitcoin FGI score + classification (2018–2025) |

**Historical Data columns used:**
`Account`, `Coin`, `Side`, `Direction`, `Closed PnL`, `Size USD`, `Fee`, `Crossed`, `Timestamp IST`

**Fear & Greed columns used:**
`date`, `value` (numeric score 0–100), `classification` (Extreme Fear → Extreme Greed)

> Datasets are not included in this repo due to size. Download links in the assignment brief.

---

## Project Structure

```
├── intern_assignment.py             # Main analysis script
├── trader_sentiment_analysis.ipynb  # Full annotated Jupyter notebook
├── trader_sentiment_report.pdf      # Final PDF report (9 pages)
├── README.md                        # This file
│
├── graphs/
│   ├── graph_avg_pnl.png            # Avg PnL by sentiment
│   ├── graph_win_rate.png           # Win rate by sentiment
│   ├── graph_trade_count.png        # Trade volume by sentiment
│   ├── graph_trade_size.png         # Avg trade size by sentiment
│   ├── graph_buy_sell_heatmap.png   # BUY vs SELL PnL heatmap
│   └── graph_top_traders.png        # Top 10 traders by total PnL
│
└── data/
    ├── pnl_summary.csv              # Aggregated PnL stats per sentiment
    ├── top_traders.csv              # Top 10 traders ranked by total PnL
    └── buy_sell_analysis.csv        # BUY vs SELL breakdown per sentiment
```

---

## Methodology

### 1. Data Cleaning
- Parsed IST timestamps (`DD-MM-YYYY HH:MM`) using `pd.to_datetime` with `.dt.normalize()`
  to strip time and create a plain date join key
- Left-joined trade data to FGI table on `date`
- Dropped ~6 boundary rows with no matching FGI date
- Treated `sentiment` as an ordered categorical: `Extreme Fear → Extreme Greed`

### 2. Analysis Approach
- **Profitability:** Mean and median `Closed PnL` grouped by sentiment
- **Win Rate:** % of `Close Long` / `Close Short` trades with `Closed PnL > 0`
- **Behaviour:** Trade size, market order % (`Crossed`), and BUY/SELL split per sentiment
- **Coin-level:** Top 10 coins by absolute PnL, broken down by sentiment (heatmap)
- **Trader-level:** Total PnL, trade count, and avg PnL per unique wallet address

### 3. Key Design Decisions
- Used **closing trades only** for win rate (open legs have `Closed PnL = 0`)
- Clipped PnL at ±$500 for box plots to prevent outliers from collapsing distributions
- Selected top coins by **absolute** total PnL (not count) — highlights coins that
  actually moved money, not just noisy low-value tickers

---

## Charts Produced

### Average PnL by Sentiment
Extreme Greed leads on raw average but has a median of $0 — driven by outlier wins.
Fear is the most *consistent* regime for profitability.

### Win Rate by Sentiment
Win rates are surprisingly uniform (37–44%), confirming that the edge lies in
**size of wins**, not frequency. Extreme Greed wins less often but bigger.

### Trade Count by Sentiment
Fear accounts for 29.5% of all trades (61,837) — traders stay active during downturns,
which is the opposite of retail behaviour.

### Average Trade Size by Sentiment
Professionals deploy **larger positions in Fear** (~$7,900) than in Extreme Greed (~$3,000).
Conviction entries when others are panicking.

### BUY vs SELL Heatmap
The single most actionable chart. SELL in Extreme Greed = $114.58 avg PnL.
BUY in Fear = $63.93 avg PnL. Everything else is secondary to these two cells.

### Top 10 Traders
Top wallet earned $2.14M — more than double #2. Returns are highly concentrated,
suggesting systematic or well-capitalised strategies dominate over discretionary trading.

---

## Strategy Recommendations

```
FGI < 25  (Extreme Fear)   →  Wait; no strong directional edge
FGI 25-44 (Fear)           →  GO LONG  | increase size | use limit orders
FGI 45-55 (Neutral)        →  Range strategies | tighter targets
FGI 56-74 (Greed)          →  Favour SHORT | tighten stops on longs
FGI > 75  (Extreme Greed)  →  GO SHORT | high-conviction sells only
```

---

## Author

**Ayush Khandelwal**
Submitted for: Primetrade.ai Data Science Internship
Email: khandelwala343@gmail.com
LinkedIn: https://www.linkedin.com/in/ayush-khandelwal-964389326/

---

*All analysis is based on historical data. Nothing here constitutes financial advice.*
