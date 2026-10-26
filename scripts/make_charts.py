"""Charts for XEQT investigation. Colours are for charts only, per her rule."""
import pandas as pd, matplotlib.pyplot as plt, pathlib
base = pathlib.Path(__file__).resolve().parents[1]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
g = pd.read_csv(base/"data"/"growth_of_10000.csv", index_col=0, parse_dates=True)
dd = pd.read_csv(base/"data"/"drawdowns.csv", index_col=0, parse_dates=True)

fig, ax = plt.subplots(figsize=(10,5.5))
for c in ["XEQT","VEQT","XGRO","VFV","XIC"]:
    ax.plot(g.index, g[c], label=c)
ax.set_title("Growth of $10,000 in CAD, weekly, 23 Aug 2019 to 23 Oct 2026")
ax.set_ylabel("$"); ax.grid(alpha=0.3); ax.legend(); fig.tight_layout()
fig.savefig(base/"charts"/"growth_of_10000.png", dpi=200); plt.close(fig)

fig, ax = plt.subplots(figsize=(10,5.5))
ax.plot(dd.index, dd["XEQT"]*100, color="#1f4e79")
ax.fill_between(dd.index, dd["XEQT"]*100, 0, alpha=0.2)
ax.set_title("XEQT drawdown: fall from the previous peak, in percent")
ax.set_ylabel("%"); ax.grid(alpha=0.3); fig.tight_layout()
fig.savefig(base/"charts"/"xeqt_drawdown.png", dpi=200); plt.close(fig)

# Underlying ETF weights, Morningstar holdings as of 23 Oct 2026
labels = ["US total market\n(XTOT, CAD-hedged)", "Canada\n(XIC)", "Developed ex North America\n(XEF)", "US total market\n(ITOT, US-listed, unhedged)", "Emerging markets\n(XEC)"]
vals = [31.20, 25.73, 23.95, 14.44, 4.55]
fig, ax = plt.subplots(figsize=(9,5))
ax.barh(labels, vals)
ax.set_title("XEQT underlying ETF weights, Morningstar, 23 Oct 2026")
ax.set_xlabel("% of XEQT")
for i, v in enumerate(vals): ax.text(v+0.6, i, f"{v:.2f}%", va="center")
ax.set_xlim(0, 36); ax.grid(axis="x", alpha=0.3); fig.tight_layout()
fig.savefig(base/"charts"/"underlying_weights.png", dpi=200); plt.close(fig)
print("charts done")
