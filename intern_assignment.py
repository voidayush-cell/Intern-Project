import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.options.display.float_format = "{:,.2f}".format

plt.style.use("ggplot")
# ============================================================
# SETTINGS
# ============================================================

plt.style.use("ggplot")

# ============================================================
# LOAD DATA
# ============================================================

print("Loading datasets...")

trades = pd.read_csv(
    "/Users/ayushkhandelwal/Downloads/historical_data.csv"
)

sentiment = pd.read_csv(
    "/Users/ayushkhandelwal/Downloads/fear_greed_index.csv"
)

print("Trades Shape:", trades.shape)
print("Sentiment Shape:", sentiment.shape)

# ============================================================
# DATE CONVERSION
# ============================================================

trades["date"] = pd.to_datetime(
    trades["Timestamp IST"],
    dayfirst=True,
    errors="coerce"
).dt.date

sentiment["date"] = pd.to_datetime(
    sentiment["date"],
    errors="coerce"
).dt.date

print("\nInvalid Trade Dates:",
      trades["date"].isna().sum())

print("Invalid Sentiment Dates:",
      sentiment["date"].isna().sum())

# ============================================================
# REMOVE DUPLICATE DATES
# ============================================================

sentiment = (
    sentiment
    .sort_values("date")
    .drop_duplicates(subset=["date"], keep="first")
)

# ============================================================
# MERGE
# ============================================================

print("\nMerging datasets...")

df = trades.merge(
    sentiment[["date", "classification", "value"]],
    on="date",
    how="left"
)

print("Merged Shape:", df.shape)

# ============================================================
# WIN COLUMN
# ============================================================

df["Win"] = (
    df["Closed PnL"] > 0
).astype(int)

# ============================================================
# PNL SUMMARY
# ============================================================

pnl_summary = (
    df.groupby("classification")["Closed PnL"]
      .agg(["count", "mean", "median", "sum"])
      .round(2)
)

print("\nPNL SUMMARY")
print(pnl_summary)

# ============================================================
# WIN RATE
# ============================================================

win_rate = (
    df.groupby("classification")["Win"]
      .mean()
      .mul(100)
      .round(2)
)

print("\nWIN RATE")
print(win_rate)

# ============================================================
# TRADE SIZE
# ============================================================

trade_size = (
    df.groupby("classification")["Size USD"]
      .mean()
      .round(2)
)

print("\nTRADE SIZE")
print(trade_size)

# ============================================================
# TRADE COUNT
# ============================================================

trade_count = (
    df.groupby("classification")
      .size()
)

print("\nTRADE COUNT")
print(trade_count)

# ============================================================
# BUY VS SELL
# ============================================================

buy_sell = pd.pivot_table(
    df,
    values="Closed PnL",
    index="classification",
    columns="Side",
    aggfunc="mean"
)

print("\nBUY VS SELL")
print(buy_sell)

# ============================================================
# TOP 10 TRADERS
# ============================================================

# ============================================================
# TOP 10 TRADERS
# ============================================================

print("\n" + "="*60)
print("TOP 10 TRADERS")
print("="*60)

top_traders = (
    df.groupby("Account")["Closed PnL"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .round(2)
)

top_traders_df = top_traders.reset_index()

top_traders_df.columns = [
    "Account",
    "Total_PnL"
]

top_traders_df["Short_Account"] = (
    top_traders_df["Account"]
    .apply(
        lambda x: x[:8] + "..." + x[-4:]
    )
)

print(
    top_traders_df[
        ["Short_Account", "Total_PnL"]
    ]
)

top_traders_df.to_csv(
    "top_traders.csv",
    index=False
)

# ============================================================
# SAVE CSV OUTPUTS
# ============================================================

pnl_summary.to_csv("pnl_summary.csv")
buy_sell.to_csv("buy_sell_analysis.csv")
top_traders.to_csv("top_traders.csv")

# ============================================================
# GRAPH 1 : AVG PNL
# ============================================================

avg_pnl = (
    df.groupby("classification")["Closed PnL"]
      .mean()
      .reset_index()
)

plt.figure(figsize=(8,5))
sns.barplot(
    data=avg_pnl,
    x="classification",
    y="Closed PnL"
)
plt.title("Average PnL by Sentiment")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("graph_avg_pnl.png")
plt.close()

# ============================================================
# GRAPH 2 : WIN RATE
# ============================================================

win_rate_plot = win_rate.reset_index()

plt.figure(figsize=(8,5))
sns.barplot(
    data=win_rate_plot,
    x="classification",
    y="Win"
)
plt.title("Win Rate by Sentiment")
plt.ylabel("Win Rate (%)")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("graph_win_rate.png")
plt.close()

# ============================================================
# GRAPH 3 : TRADE SIZE
# ============================================================

size_plot = trade_size.reset_index()

plt.figure(figsize=(8,5))
sns.barplot(
    data=size_plot,
    x="classification",
    y="Size USD"
)
plt.title("Average Trade Size by Sentiment")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("graph_trade_size.png")
plt.close()

# ============================================================
# GRAPH 4 : TRADE COUNT
# ============================================================

plt.figure(figsize=(8,5))
trade_count.plot(kind="bar")
plt.title("Trade Count by Sentiment")
plt.tight_layout()
plt.savefig("graph_trade_count.png")
plt.close()

# ============================================================
# GRAPH 5 : TOP TRADERS
# ============================================================
# ============================================================
# GRAPH 5 : TOP TRADERS
# ============================================================

graph_df = top_traders_df.copy()

graph_df["Rank"] = [
    f"Trader {i}"
    for i in range(
        1,
        len(graph_df) + 1
    )
]

plt.figure(figsize=(10,6))

plt.barh(
    graph_df["Rank"],
    graph_df["Total_PnL"]
)

plt.title(
    "Top 10 Traders by Total PnL"
)

plt.xlabel(
    "Total Closed PnL (USD)"
)

plt.tight_layout()

plt.savefig(
    "graph_top_traders.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ============================================================
# GRAPH 6 : BUY VS SELL HEATMAP
# ============================================================

plt.figure(figsize=(8,5))
sns.heatmap(
    buy_sell,
    annot=True,
    fmt=".2f"
)
plt.title("Buy vs Sell Performance")
plt.tight_layout()
plt.savefig("graph_buy_sell_heatmap.png")
plt.close()

# ============================================================
# COMPLETED
# ============================================================

print("\nANALYSIS COMPLETED SUCCESSFULLY")
print("Graphs and CSV files generated.")