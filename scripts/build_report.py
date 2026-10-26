"""XEQT report PDF. Black text only. Charts may use colour. No first person.
Name appears only on the title line."""
import pathlib
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib import colors
base = pathlib.Path(__file__).resolve().parents[1]
styles = getSampleStyleSheet()
body = ParagraphStyle("body", parent=styles["Normal"], fontName="Helvetica", fontSize=10.5, leading=15, textColor=colors.black, spaceAfter=6)
h1 = ParagraphStyle("h1", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=colors.black, spaceBefore=12, spaceAfter=8)
h2 = ParagraphStyle("h2", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=12.5, leading=16, textColor=colors.black, spaceBefore=10, spaceAfter=6)
small = ParagraphStyle("small", parent=styles["Normal"], fontName="Helvetica", fontSize=9, leading=12, textColor=colors.black, spaceAfter=4)
def P(t, s=body): return Paragraph(t, s)
def tbl(data, widths):
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#DDDDDD")),
        ("TEXTCOLOR", (0,0), (-1,-1), colors.black),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("GRID", (0,0), (-1,-1), 0.4, colors.black),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 5), ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    return t
def img(name, w=170*mm):
    return Image(str(base/"charts"/name), width=w, height=w*0.55)
story = []
story.append(P("Investigating XEQT: What One Ticker Buys, What It Costs, and What Risk It Carries", h1))
story.append(P("Munzeleen Sarwar", body))
story.append(P("iShares Core Equity ETF Portfolio, TSX: XEQT. Price data to 23 October 2026. This report is an investigation, not personal investment advice.", small))
story.append(P("Summary", h1))
story.append(P("XEQT is one fund that holds five other index funds. Together, those funds hold thousands of stocks in Canada, the United States, developed markets outside North America, and emerging markets. The target mix is 100% stocks and no bonds. BlackRock rebalances the mix. The buyer does not need to rebalance it."))
story.append(P("The main findings are simple. First, XEQT and its closest rival, VEQT, produced almost the same result over the full period in this report. Second, XEQT fell hard in a crash, because 100% stocks means no bond cushion. Third, XEQT is cheap compared with a typical mutual fund, and only slightly more expensive than building the same mix from separate ETFs. Fourth, the cost saving from building the mix by hand is small, and it comes with extra trading, extra time, and extra tax records."))
story.append(P("Key facts", h2))
story.append(tbl([
["Item","Detail"],
["Launch date","7 August 2019"],
["Target mix","100% equity, 0% bonds"],
["Management expense ratio","0.20% per year (February 2026 factsheet)"],
["Management fee","0.17% per year after the reduction effective 18 December 2025"],
["Distributions","Quarterly"],
["12 month trailing yield, February 2026","1.58%"],
["Net assets, February 2026","14,832.65 million CAD"],
["Price, weekly close 23 October 2026","44.84 CAD (Yahoo Finance adjusted close)"],
], [62*mm, 108*mm]))
story.append(P("1. What XEQT buys", h1))
story.append(P("XEQT does not buy thousands of stocks directly. It buys five underlying ETFs. Each underlying ETF then holds its own basket of stocks. This is why the headline number of stocks is large, while the number of direct holdings in XEQT is only five."))
story.append(tbl([
["Fund","What it holds","Weight, 23 Oct 2026"],
["XTOT","US stocks, CAD-hedged","31.20%"],
["XIC","Canadian stocks","25.73%"],
["XEF","Developed markets outside North America","23.95%"],
["ITOT","US stocks, US-listed, unhedged","14.44%"],
["XEC","Emerging market stocks","4.55%"],
["Cash","Cash","0.14%"],
], [28*mm, 102*mm, 40*mm]))
story.append(P("Source for weights: Morningstar XEQT portfolio page, holdings as of 23 October 2026. Weights move as prices move and as BlackRock rebalances. The target mix in the fund documents is 25% Canada, 45% United States, 25% developed markets outside North America, and 5% emerging markets. The October snapshot is close to that target. The United States total in the snapshot is 45.64%, which is 31.20% in XTOT, the CAD-hedged fund, plus 14.44% in ITOT, the US-listed unhedged fund. Full fund names are: XTOT, iShares Core S and P Total US Stock Market Index ETF (CAD-hedged); XIC, iShares Core S and P/TSX Capped Composite Index ETF; XEF, iShares Core MSCI EAFE IMI Index ETF; ITOT, iShares Core S and P Total US Stock Market ETF; XEC, iShares Core MSCI Emerging Markets IMI Index ETF."))
story.append(img("underlying_weights.png"))
story.append(P("Two points matter here. First, buying XEQT is not the same as buying 8,300 stocks in equal amounts. Most of the money is still in large companies in the United States, Canada, Europe, and Japan, because those markets are large. Second, part of the United States exposure is hedged to Canadian dollars. Hedging reduces the effect of US dollar moves on that part. The unhedged part still moves with the US dollar."))
story.append(P("The top individual stocks on 6 October 2026 were NVIDIA at 3.52%, Apple at 2.96%, Microsoft at 2.39%, Royal Bank of Canada at 1.89%, and Amazon at 1.53%. The top 10 stocks together were about 18.3% of XEQT. That point matters. Even with about 8,300 underlying stocks, the largest companies still carry a large share of the fund, because the fund follows market size."))
story.append(P("2. How XEQT performed", h1))
story.append(P("The table below uses weekly prices in Canadian dollars from 23 August 2019 to 23 October 2026, a total of 375 weeks. Prices are adjusted for dividends and splits. Annual return is the average weekly return multiplied by 52. Volatility is the standard deviation of weekly returns multiplied by the square root of 52. Sharpe ratio uses a stated 2.0% risk free rate, because a daily Canadian T-bill series was not in this download. Return divided by volatility is also shown, because it needs no risk free assumption."))
story.append(tbl([
["Fund","Annual return","Volatility","Return / volatility","Sharpe","Max fall","$10,000 becomes"],
["XEQT","14.33%","14.83%","0.97","0.83","-27.77%","$25,915"],
["VEQT","14.31%","14.67%","0.98","0.84","-28.60%","$25,917"],
["XGRO","11.68%","12.24%","0.95","0.79","-23.93%","$21,975"],
["VFV (US only)","16.66%","15.85%","1.05","0.92","-25.94%","$30,298"],
["XIC (Canada only)","14.96%","15.51%","0.96","0.84","-33.22%","$26,889"],
], [28*mm, 26*mm, 24*mm, 30*mm, 18*mm, 22*mm, 22*mm]))
story.append(img("growth_of_10000.png"))
story.append(P("Over the full period, XEQT turned $10,000 into $25,915. VEQT turned $10,000 into $25,917, a difference of $2. That result should not be read as proof that the two funds are identical in every period. It means that, over this long period, their different country mixes and different providers produced almost the same total result. The United States only fund, VFV, produced more, at $30,298, but with higher volatility. The Canada only fund, XIC, produced $26,889, but with the largest fall in the group."))
story.append(P("2.1 Other all-equity funds in Canada", h2))
story.append(P("XEQT is not the only all-equity fund in Canada. The table below lists the main peers. Management fee and MER are not the same thing. Management fee is the fee charged by the manager. MER is the total expense ratio reported after taxes and other fund costs. That is why the two numbers differ for the same fund."))
story.append(tbl([
["Fund","Provider and type","Fee"],
["XEQT","BlackRock iShares. Passive, broad market index, fund of funds.","MER 0.20%. Management fee 0.17%."],
["VEQT","Vanguard. Passive global equity, standard market cap indexes.","MER 0.24% in recent comparisons. Management fee recently cut to 0.17%, so the reported MER may fall at the next reporting date."],
["ZEQT","BMO. Passive, low cost all-equity fund of funds.","MER 0.20%. Management fee 0.15%."],
["HEQT","Global X. Fund of funds holding Global X index ETFs.","Expense ratio 0.24%. Management fee 0.18%."],
["TEQT","TD. All-equity asset allocation, fund of funds.","Management fee 0.15%. MER about 0.17% in recent comparisons."],
["CAGE","CIBC, sub-advised by Avantis. Rules-based active fund, with a tilt to cheaper and more profitable companies. This fund is not a passive cap-weighted index fund.","Management fee 0.28%. First interim annualised MER 0.35% at 30 June 2026. The MER is not yet settled, because the fund launched in March 2026."],
], [22*mm, 78*mm, 70*mm]))
story.append(P("A full period return comparison back to 2019 is not possible for this peer group. TEQT launched in April 2025 and CAGE launched on 18 March 2026. The table below therefore uses only the short common window from 20 March 2026 to 23 October 2026, a total of 31 weekly returns. This window is too short to rank the funds. It is shown only to show that, in that short window, the peers moved closely together."))
story.append(tbl([
["Fund","Total gain, Mar to Oct 2026","Volatility, annualised"],
["XEQT","16.90%","11.10%"],
["VEQT","16.81%","11.33%"],
["ZEQT","17.16%","11.34%"],
["HEQT","18.08%","11.59%"],
["TEQT","17.97%","11.04%"],
["CAGE","16.26%","10.40%"],
], [40*mm, 65*mm, 65*mm]))
story.append(P("The main difference between the peers is therefore not short term return. It is fee, country mix, whether the fund follows market size or applies a factor tilt, and how long the fund has existed. CAGE is the clear outlier on method and cost. It charges more and it deliberately tilts away from market size. The other five peers are closer to each other on method, with fees from about 0.17% to 0.24% on the measures above."))
story.append(P("3. Risk in plain terms", h1))
story.append(P("Volatility measures how much weekly returns move around their average. XEQT volatility was 14.83% per year. That is a normal level for a 100% stock portfolio. It is lower than Canada only at 15.51% and the United States only at 15.85%, which is the benefit of holding several regions at once. It is higher than XGRO at 12.24%, because XGRO holds 20% bonds."))
story.append(P("Maximum drawdown measures the largest fall from a previous peak to a later low. For XEQT, the largest fall was 27.77%, and it happened on 20 March 2020, during the COVID-19 crash. In plain terms, $10,000 at the previous peak fell to about $7,223 at the low, before recovering. XGRO fell less, at 23.93%, because bonds softened the fall. XIC fell more, at 33.22%."))
story.append(img("xeqt_drawdown.png"))
story.append(P("Weekly CVaR at 95% measures the average loss in the worst 5% of weeks. For XEQT, that average was a loss of 4.66% in a bad week. For XGRO, it was 3.85%. For XIC, it was 5.24%. CVaR is useful because it looks only at bad weeks. Volatility looks at good and bad weeks together. A portfolio can look calm on average and still lose a lot in a bad week."))
story.append(P("Calendar years show the same point from a different angle. XEQT gained 10.56% in 2020, lost 10.99% in 2022, gained 17.27% in 2023, gained 25.76% in 2024, and gained 19.92% in 2025, using Yahoo adjusted weekly prices. The official factsheet calendar returns differ slightly, because official returns use net asset value and different dates. For example, the factsheet reports 2024 at 24.67% and 2022 at 10.93% loss. Small differences of this kind are expected when the price source changes. The direction and size of each year are the same."))
story.append(P("4. XEQT against its neighbours", h1))
story.append(P("VEQT is the closest comparison. It is the Vanguard all-equity portfolio. Over the full period, XEQT and VEQT had almost the same return, almost the same volatility, and a weekly correlation of 0.979, where 1.00 means they move together exactly. For most practical purposes in this period, choosing between them changed very little. The remaining differences are provider, exact country weights, and fee. VEQT has a slightly higher fee in recent third-party checks, at 0.22% against 0.20% for XEQT, but fees change and should be checked at the time of any decision."))
story.append(P("XGRO is the calmer neighbour. It holds 80% stocks and 20% bonds. Over the full period, it returned less, at 11.68% per year against 14.33% for XEQT, but it also fell less in 2020 and in 2022. That trade is the point of bonds. A lower return in good years buys a smaller fall in bad years."))
story.append(P("VFV is the United States only neighbour. It returned more over the full period, but that result depends on the United States leading the world in that period. In 2025, the pattern reversed. XIC gained 32.50% in 2025, while VFV gained 11.14%. A single-country fund can lead for years and then lag for years. XEQT avoids a single-country bet by holding all regions, but it also gives up the extra gain when one region leads."))
story.append(P("5. Cost: XEQT, building it by hand, and a mutual fund", h1))
story.append(P("XEQT charges 0.20% per year. On $100,000, that is $200 per year. The fee is taken inside the fund, so the holder does not pay a separate bill."))
story.append(P("Building the same mix by hand means buying the underlying ETFs separately. Using the October weights and the underlying fund fees reported by Morningstar, the weighted fee is about 0.12% per year, or about $115 per year on $100,000. The saving is about $85 per year on $100,000. That is real, but it is small."))
story.append(tbl([
["Option","Fee per year","Fee on $100,000 per year","Illustrative value after 20 years"],
["XEQT at 0.20%","0.20%","$200","$372,756"],
["Separate ETFs at about 0.12%","0.12%","$115","$378,735"],
["Mutual fund at 2.00%, illustration only","2.00%","$2,000","$265,330"],
], [58*mm, 28*mm, 42*mm, 42*mm]))
story.append(P("The illustration assumes a constant gross return of 7% per year, which never happens in practice. It is shown only to make the fee difference visible. After 20 years, the separate ETF mix is ahead by $5,979 on $100,000 in this illustration, before trading costs, time, and tax records. The mutual fund illustration is behind by $107,426, which shows why a 2% fee matters far more than a 0.08% fee difference."))
story.append(P("Building by hand also has costs that are not in the fee. Each rebalance needs trades. Each trade can have a spread, which is the gap between the buy price and the sell price. The holder must track the weights, decide when to rebalance, and keep tax records for each fund. XEQT does that work inside one fund. For many holders, $85 per year on $100,000 is a reasonable price for that work. For a large account, the saving grows in dollars, and building by hand becomes more attractive, if the holder will actually rebalance."))
story.append(P("6. Control: what XEQT does not let the holder change", h1))
story.append(P("XEQT fixes three things. First, the country mix is fixed near 25% Canada, 45% United States, 25% developed markets outside North America, and 5% emerging markets. Second, the stock and bond mix is fixed at 100% stocks. Third, the sector mix follows the market, not a personal view."))
story.append(P("Control helps in some years and hurts in others. In 2022, Canada fell less than the world. XIC lost 5.82% in that calendar year, while XEQT lost 10.99%. A holder who had shifted more money to Canada before 2022 would have lost less. In 2024, the opposite happened. VFV gained 37.63%, while XIC gained 21.70%. A holder who had shifted more money to Canada before 2024 would have gained less. Control is only useful if the holder can make the right shift before the year starts. Most holders cannot do that reliably."))
story.append(P("Currency is part of control as well. Most of XEQT is not hedged, so a fall in the Canadian dollar raises the Canadian dollar value of foreign stocks, and a rise in the Canadian dollar lowers it. The hedged part of the United States exposure, 31.20% of XEQT in October 2026 in XTOT, removes currency moves from that part only. The unhedged ITOT part, 14.44%, still moves with the US dollar. The holder cannot change the hedged share in XEQT."))
story.append(P("Distributions and tax need a short note. XEQT pays distributions quarterly. The 12 month trailing yield was 1.58% in February 2026. Distributions are taxable in a non-registered account, and the type of distribution matters. Foreign withholding tax can also apply inside the underlying funds. The size of that effect depends on the account type and the holder's tax situation. This report does not give personal tax advice. A holder should check the tax treatment for a registered account and a non-registered account separately."))
story.append(P("7. Verdict: who XEQT fits, and who it does not fit", h1))
story.append(P("XEQT fits a holder who meets all of these points. The money is for the long term, at least 10 years and preferably longer. The holder can accept a fall of about 28% from a peak, as happened in March 2020, without selling. The holder wants global diversification in one fund and does not want to rebalance. The holder accepts that the return will follow the world stock market, including bad years."))
story.append(P("XEQT does not fit a holder who needs the money in the next few years. It does not fit a holder who needs regular income, because the yield is about 1.6% and it varies. It does not fit a holder who needs bonds to reduce falls, because XEQT holds no bonds. For that holder, XGRO, with 20% bonds, is a closer fit, at the cost of lower long term return. It also does not fit a holder who wants to set a different country mix, for example more Canada or less United States, because XEQT fixes that mix."))
story.append(P("The final point is about comparison. XEQT should not be judged by one good year or one bad year. Over the full period in this report, it delivered a high return with high volatility, almost the same as VEQT, less than the United States only fund in a period when the United States led, and more than the bond mix in a period when stocks did well. That is what a 100% global stock fund is expected to do. The value of XEQT is not that it beats every other fund. The value is that it gives a complete global stock portfolio in one ticker, at a low fee, with rebalancing done inside the fund."))
story.append(P("8. What was learned from this project", h1))
story.append(P("1. One ticker can be a whole portfolio, but it is not magic. XEQT holds five funds, which hold about 8,300 stocks. Most of the money is still in large companies in the United States, Canada, Europe, and Japan, because the fund follows market size. The top 10 stocks alone were about 18.3% of the fund."))
story.append(P("2. Diversification helped, but it did not remove crashes. XEQT was less volatile than Canada only or the United States only. It still fell 27.77% from peak to low in March 2020. A 100% stock fund has no bond cushion, so a holder has to be able to sit through that kind of fall."))
story.append(P("3. The closest rival was almost identical. Over more than seven years, XEQT turned $10,000 into $25,915 and VEQT turned it into $25,917. For a long term holder, picking between two good global all-equity funds mattered far less than staying invested."))
story.append(P("4. Fees matter, but small fee gaps matter less than people think. XEQT costs 0.20% per year. Building the same mix from separate ETFs costs about 0.12%, saving about $85 per year on $100,000. That saving is real, but it comes with extra trades, time, and tax records. A 2% mutual fund fee, by contrast, would have cost far more over 20 years in the illustration."))
story.append(P("5. Management fee and MER are not the same number. Management fee is what the manager charges. MER is the total reported expense after taxes and other fund costs. Mixing those two up makes a fund look cheaper or more expensive than it really is."))
story.append(P("6. Control cuts both ways. XEQT fixes the country mix and fixes stocks at 100%. In 2022, Canada fell less, so more Canada would have helped. In 2024, the United States led, so more Canada would have hurt. Having control only helps if the right shift can be made before the year starts."))
story.append(P("7. New funds cannot be ranked on a short window. TEQT launched in April 2025 and CAGE launched in March 2026, so a return comparison back to 2019 was impossible. In the short common window from March to October 2026, all six peers were close, from 16.26% to 18.08%. That window was too short to call a winner."))
story.append(P("8. Details need checking, even in a simple fund. The first version of this report labelled the two United States funds backwards. XTOT at 31.20% is the CAD-hedged fund, and ITOT at 14.44% is the unhedged US-listed fund. Fixing that changed the currency conclusion too. A clean table is not the same as a correct table."))
story.append(P("Limits and method", h1))
story.append(P("Price data are Yahoo Finance adjusted closes, weekly, Friday, from 23 August 2019 to 23 October 2026. Official net asset value returns differ slightly. Holdings weights are a snapshot, not a permanent mix. The Sharpe ratio uses a stated 2.0% risk free rate, not a market T-bill series. Cost illustrations assume a constant 7% gross return, which is a teaching assumption, not a forecast. Past performance does not predict future performance. Sector weights are not reported in this investigation, because the February 2026 factsheet extraction did not include a reliable sector table, and third-party sector tables for XEQT differ by date and method. Geographic weights and underlying ETF weights are reported instead, because those are verified from the factsheet and Morningstar."))
story.append(P("Sources", h1))
story.append(P("iShares Core Equity ETF Portfolio factsheet, February 2026, data as at 28 February 2026. Morningstar XEQT portfolio page, holdings as of 23 October 2026. Yahoo Finance adjusted closes for XEQT.TO, VEQT.TO, XGRO.TO, VFV.TO, XIC.TO, ZEQT.TO, HEQT.TO, TEQT.TO, and CAGE.TO. Peer fees are from provider and third-party comparisons checked in October 2026, and are labelled as management fee or MER where the source makes that distinction. Scripts, data, and the Excel model are in the project folder, so every number in the performance tables can be recomputed from the weekly price file."))
doc = SimpleDocTemplate(str(base/"XEQT_Investigation_Report.pdf"), pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=18*mm, bottomMargin=18*mm, title="Investigating XEQT", author="Munzeleen Sarwar")
doc.build(story)
print("report done")
