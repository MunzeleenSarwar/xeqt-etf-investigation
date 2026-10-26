"""XEQT investigation: download CAD weekly prices, compute return and risk.
Sources: Yahoo Finance adjusted closes. XEQT inception Aug 2019, so the common
window starts at the first full week after inception for all tickers.
Risk free rate for Sharpe: 2.0% per year, stated as a simple constant assumption
because a daily Canadian T-bill series is not in this download. Return/volatility
is also shown, which needs no risk free assumption.
"""
import numpy as np, pandas as pd, yfinance as yf, json, pathlib
base = pathlib.Path(__file__).resolve().parents[1]
tickers = {"XEQT": "XEQT.TO", "VEQT": "VEQT.TO", "XGRO": "XGRO.TO",
           "VFV": "VFV.TO", "XIC": "XIC.TO"}
# XIC is used as the Canada proxy. The Yahoo TSX index ticker returned no data
# on this run, so it is not used. XIC tracks the S&P/TSX Capped Composite.
frames = []
for name, sym in tickers.items():
    d = yf.download(sym, start="2019-08-07", end="2026-10-24",
                    auto_adjust=True, progress=False, timeout=60)["Close"]
    d.columns = [name]
    frames.append(d)
prices = pd.concat(frames, axis=1)
prices.columns = list(tickers.keys())
prices = prices.dropna(how="all")
weekly = prices.resample("W-FRI").last().dropna()
weekly.to_csv(base/"data"/"weekly_prices_cad.csv")
rets = weekly.pct_change().dropna()
rets.to_csv(base/"data"/"weekly_returns.csv")

def stats(s, rf=0.02):
    ann_ret = s.mean()*52
    vol = s.std()*np.sqrt(52)
    sharpe = (ann_ret-rf)/vol
    cum = (1+s).cumprod()
    dd = cum/cum.cummax()-1
    cvar = s[s <= s.quantile(0.05)].mean()*np.sqrt(52)  # weekly tail mean, annualised by sqrt for comparability note in report; also weekly below
    return {
        "start": str(s.index[0].date()), "end": str(s.index[-1].date()), "weeks": int(len(s)),
        "annual_return_pct": round(float(ann_ret*100),2),
        "annual_vol_pct": round(float(vol*100),2),
        "return_vol": round(float(ann_ret/vol),2),
        "sharpe_rf2pct": round(float(sharpe),2),
        "max_drawdown_pct": round(float(dd.min()*100),2),
        "worst_week_pct": round(float(s.min()*100),2),
        "weekly_cvar95_pct": round(float(s[s <= s.quantile(0.05)].mean()*100),2),
        "cumulative_pct": round(float((cum.iloc[-1]-1)*100),2),
        "final_10000": round(float(10000*cum.iloc[-1]),2),
    }

out = {k: stats(rets[k]) for k in rets.columns}
# Subperiods: calendar years and stress windows
def period_stats(s, a, b):
    x = s.loc[a:b]
    if len(x) < 10: return None
    return {"weeks": int(len(x)), "return_pct": round(float(x.mean()*52*100),2),
            "vol_pct": round(float(x.std()*np.sqrt(52)*100),2),
            "cum_pct": round(float(((1+x).prod()-1)*100),2)}
periods = {
    "2020": ("2020-01-01","2020-12-31"), "2022": ("2022-01-01","2022-12-31"),
    "2023": ("2023-01-01","2023-12-31"), "2024": ("2024-01-01","2024-12-31"),
    "2025": ("2025-01-01","2025-12-31"),
    "2020_crash_feb_mar": ("2020-02-21","2020-03-31"),
    "last_3y": ("2023-10-27","2026-10-23"), "last_5y": ("2021-10-22","2026-10-23"),
    "full": (str(rets.index[0].date()), str(rets.index[-1].date())),
}
sub = {p: {k: period_stats(rets[k], a, b) for k in rets.columns} for p,(a,b) in periods.items()}
# Growth of 10000 and drawdown series for charts
growth = (1+rets).cumprod()*10000
growth.to_csv(base/"data"/"growth_of_10000.csv")
dd = growth/growth.cummax()-1
dd.to_csv(base/"data"/"drawdowns.csv")
# Correlations with XEQT
corr = rets.corr()["XEQT"].round(3).to_dict()
# Rolling 1y return for XEQT at end
result = {"metrics": out, "periods": sub, "corr_with_xeqt": corr,
          "first_price": {k: round(float(weekly[k].iloc[0]),2) for k in weekly.columns},
          "last_price": {k: round(float(weekly[k].iloc[-1]),2) for k in weekly.columns}}
with open(base/"data"/"metrics.json","w") as f: json.dump(result, f, indent=2)
print(json.dumps(result, indent=2))
