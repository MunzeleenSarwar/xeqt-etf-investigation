# Investigating XEQT

## Question
What does one ticker buy, what does it cost, what risk does it carry,
and when would building a portfolio by hand beat it?

## Answer in one paragraph
XEQT is a 100% stock fund that holds five underlying index funds.
Over 23 August 2019 to 23 October 2026, $10,000 in XEQT became $25,915,
almost the same as VEQT at $25,917. XEQT fell 27.77% from peak to low
in March 2020. XEQT charges 0.20% per year. Building the same mix
from separate ETFs costs about 0.12% per year in fees, a saving of
about $85 per year on $100,000, before trading costs, time, and tax records.

## Files
- XEQT_Investigation_Report.pdf: 8 page report, plain language, including a Lessons Learned section.
- XEQT_Investigation_Model.xlsx: performance, holdings, calendar, cost, sources, peers.
- XEQT_Investigation_Notebook.ipynb: recomputation notebook.
- data/: weekly prices, weekly returns, growth, drawdowns, metrics.
- charts/: growth, drawdown, underlying weights.
- scripts/: download and analysis, charts, Excel, report.

## Method and limits
Weekly Friday prices in CAD from Yahoo Finance, adjusted for dividends.
Sharpe uses a stated 2.0% risk free rate, not a market T-bill series.
Holdings weights are a Morningstar snapshot at 23 October 2026.
The February 2026 iShares factsheet is the source for MER and launch facts.
Cost illustrations assume a constant 7% gross return, which is a teaching
assumption, not a forecast. Past performance does not predict future performance.
This project is an investigation, not personal investment advice.
