# Stock Price Forecasting in an Inflationary market using Artificial Neural Networks


## Introduction
- For many business analysts and researchers, forecasting stock market prices has always been a difficult task. 
- We compare multiple methods of forecasting the price of a singular stock In this instance, we will be focusing on forecasting Google’s (ticker symbol GOOG) stock price. 
- Correlated stocks considered are Amazon, Apple and the S&P500 index (ticker symbols AMZN, AAPL, SPY respectively). 
- We use permutations and combinations of relative strength index, inflation data and closing prices of other related stocks as inputs. 

## Data
- Collected data from Yahoo Finance for various stocks from the day of listing for stocks of Google, Apple, Amazon and S&P 500 from 2004 to 2022.
- Identified Closing price as the parameter that represents the overall value of the stock.
- Scaled the data to the range -1 to 1 to provide as input to the model.
- Identified Apple, Amazon and S&P 500 as the correlated stocks based the overall movement over the years and duration of the stock being listed on the market.




Stock data for Google, Amazon, Apple and S&P500 are download in code from yfinance. However, RSI and Inflation data need to be imported which are provided in this folder.

The package requirements are as follows(can be installed with pip command): 
- yfinance
- numpy
- pandas
- sklearn
- matplotlib
- torch
- seaborn
