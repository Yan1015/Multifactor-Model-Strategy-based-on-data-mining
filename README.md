# Multifactor-Model-Strategy-based-on-data-mining
## Introduction
This project aims to find the factors which can explain the stock return patterns in Chinese stock market using data mining.

I focus on fundamental-based variables, i.e., variables derived from financial statements. I used them to construct a “universe” of fundamental signals by using permutational arguments. The ability to construct such a universe is important because in order to account for the effects of data mining, one should not only include variables that were reported, but also variables that were considered but unreported. And the unreported one can be constructed by the financial statement variables.
## Data
I downloaded the infomation of three main financial statements including Balance Sheet Statement, Income Statement and Cash Flows Statement for all the stocks(company) in Chinese stock market from 2007 to 2016. And delete the financial variables which have more than 30% missing data and there are 65 accounting variables left.

## Methodology
For the remaining 65 accounting variables, we make them as X variables. From the 65 X variables, we chose 13 variables as Y variables which are Total cssets, Total current Assets, Inventory, Property, plant and equipment, Total liabilities, Total current liabilities, Long-term debt, Total common equity, Total sale, Cost of goods sold, Selling, general and adminstrative cost, Number of emplogees and Market capitalization. We chose Y variables to construct financial signals, because financial statement variables are typically more meaningful when they are compared with other accounting variables. 

For the X variables and Y variables, we constructed financial signals by calculating financial ratio (X/Y), year-to-year change (Δ in X/Y), percentage change in financial ratios (%Δ in X/Y), percentage change in each accounting variable (%Δ in X), the difference between the percentage change in each accounting variable and the percentage change in a base variable (%Δ in X - %Δ in Y), and the change in each accounting variable scaled by a lagged base variable (ΔX/lagY). So eventually we would get 65 * 13 * 5 + 65 = 4290 signals. This is where data mining comes from.

For each financial signal, we need to test whether it can explain the future stock returns. So we constructed th long-short portfolio by sorting the financial signal. and separating the stocks into 10 groups based on the rank for financial signal. So the first group is the stocks with maximum financial signal and the last group  with minimum financial signal.

For the portfolio, we calculate the annulize returns. If the returns is monotonically decreasing or increasing, it means the financial signal can perfectly explain the future stock returns.

## Code Structure
The form_signal.py is to construct the finacnial signals from the X and Y accounting variables.
The other 3 files are responsible for calculating the return for all the portfolios.

## Reference
[Fundamental Analysis and the Cross-Section of Stock Returns:
A Data-Mining Approach] 

by Xuemin (Sterling) Yan; Lingling Zheng
