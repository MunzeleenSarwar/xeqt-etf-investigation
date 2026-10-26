"""Excel model for XEQT investigation."""
import json, pathlib
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
base = pathlib.Path(__file__).resolve().parents[1]
m = json.loads((base/"data"/"metrics.json").read_text())
wb = Workbook()
hdr_fill = PatternFill("solid", fgColor="222222")
hdr_font = Font(bold=True, color="FFFFFF", size=11)
title_font = Font(bold=True, size=14)
def sheet(name, title, rows, widths):
    ws = wb.active if len(wb.sheetnames)==1 and wb.active.title=="Sheet" else wb.create_sheet(name)
    if ws.title != name: ws.title = name
    ws["A1"] = title; ws["A1"].font = title_font
    for j, h in enumerate(rows[0], 1):
        c = ws.cell(row=3, column=j, value=h); c.font = hdr_font; c.fill = hdr_fill
    for i, r in enumerate(rows[1:], 4):
        for j, v in enumerate(r, 1): ws.cell(row=i, column=j, value=v)
    for j, w in enumerate(widths, 1): ws.column_dimensions[get_column_letter(j)].width = w
    return ws
metrics = [["Fund","Annual return %","Volatility %","Return / volatility","Sharpe (2% risk free)","Max drawdown %","Worst week %","Weekly CVaR 95% %","Total gain %","$10,000 becomes $"]]
for k, v in m["metrics"].items():
    metrics.append([k, v["annual_return_pct"], v["annual_vol_pct"], v["return_vol"], v["sharpe_rf2pct"], v["max_drawdown_pct"], v["worst_week_pct"], v["weekly_cvar95_pct"], v["cumulative_pct"], v["final_10000"]])
sheet("Performance", "Performance, weekly CAD, 23 Aug 2019 to 23 Oct 2026 (375 weeks)", metrics, [12,16,14,18,20,16,14,18,14,16])
hold = [["Underlying ETF","What it holds","Weight 23 Oct 2026 % (Morningstar)"],
["XTOT - iShares Core S and P Total US Stock Market Index ETF (CAD-hedged)","US stocks, CAD-hedged","31.20"],
["iShares Core S and P/TSX Capped Composite ETF (XIC)","Canadian stocks","25.73"],
["iShares Core MSCI EAFE IMI ETF (XEF)","Developed markets outside North America","23.95"],
["ITOT - iShares Core S and P Total US Stock Market ETF","US stocks, US-listed, unhedged","14.44"],
["iShares Core MSCI Emerging Markets IMI ETF (XEC)","Emerging market stocks","4.55"],
["Cash","Cash","0.14"]]
sheet("Holdings", "XEQT underlying holdings", hold, [58,48,32])
cal = [["Year","XEQT total %","VEQT total %","XGRO total %","VFV total %","XIC total %"]]
for y in ["2020","2022","2023","2024","2025"]:
    cal.append([y] + [m["periods"][y][k]["cum_pct"] for k in ["XEQT","VEQT","XGRO","VFV","XIC"]])
sheet("Calendar", "Calendar year total return, Yahoo adjusted weekly prices", cal, [10,16,16,16,16,16])
cost = [["Option","Annual fee %","Fee on $100,000 per year $","Illustrative $100,000 after 20 years at 7% gross $"],
["XEQT","0.20","200","372,756"],
["DIY mix of underlying ETFs, weighted MER about 0.12%","0.12","115","378,735"],
["Mutual fund at 2.00% (illustration only)","2.00","2,000","265,330"]]
sheet("Cost", "Cost illustration only. Gross return is assumed constant at 7% and never happens in practice.", cost, [58,16,28,48])
src = [["Item","Source and date"],
["MER, launch date, target allocation, Feb 2026 factsheet","iShares Core Equity ETF Portfolio factsheet, February 2026, data as at 28 Feb 2026"],
["Underlying weights","Morningstar XEQT portfolio page, holdings as of 23 Oct 2026"],
["Price history and risk measures","Yahoo Finance adjusted closes, weekly Friday, 23 Aug 2019 to 23 Oct 2026"],
["Sharpe risk free rate","2.0% per year, stated assumption, not a market series"]]
sheet("Sources", "Sources and method notes", src, [52,90])
peers = [["Fund","Provider and type","Fee"],
["XEQT","BlackRock iShares. Passive, broad market index, fund of funds.","MER 0.20%. Management fee 0.17%."],
["VEQT","Vanguard. Passive global equity, standard market cap indexes.","MER 0.24% in recent comparisons. Management fee recently cut to 0.17%."],
["ZEQT","BMO. Passive, low cost all-equity fund of funds.","MER 0.20%. Management fee 0.15%."],
["HEQT","Global X. Fund of funds holding Global X index ETFs.","Expense ratio 0.24%. Management fee 0.18%."],
["TEQT","TD. All-equity asset allocation, fund of funds.","Management fee 0.15%. MER about 0.17% in recent comparisons."],
["CAGE","CIBC, sub-advised by Avantis. Rules-based active, value and profitability tilt.","Management fee 0.28%. First interim annualised MER 0.35% at 30 June 2026."]]
sheet("Peers", "All-equity peers. Short common window Mar to Oct 2026: XEQT 16.90%, VEQT 16.81%, ZEQT 17.16%, HEQT 18.08%, TEQT 17.97%, CAGE 16.26%. Window is too short to rank funds.", peers, [12,72,62])
wb.save(base/"XEQT_Investigation_Model.xlsx")
print("excel done")
