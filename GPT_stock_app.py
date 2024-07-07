import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
from pytz import timezone
import matplotlib.pyplot as plt
import seaborn as sns


# Function to check if the market is open
def is_market_open():
    market_open_time = datetime.now(timezone('US/Eastern')).replace(hour=9, minute=30, second=0, microsecond=0)
    market_close_time = datetime.now(timezone('US/Eastern')).replace(hour=16, minute=0, second=0, microsecond=0)
    now = datetime.now(timezone('US/Eastern'))
    return market_open_time <= now <= market_close_time


# Function to get historical stock data
def get_stock_data(ticker, period='1y'):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    return hist


# Function to get current stock price
def get_current_stock_price(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period='1d', interval='1m')
    return round(hist['Close'][-1], 2) if not hist.empty else None


# Function to calculate percentage differences
def calculate_percentage_differences(current_price, prices):
    return [(current_price - price) / price * 100 for price in prices]


# Main app
st.title("Stock Analysis App")
st.write("This app fetches stock data and displays a heatmap of price differences.")

stocks = st.multiselect("Select stocks", ["IVV", "VNQ", "VWO", "BNDX", "VEUR.AS"])
periods = ['1mo', '3mo', '6mo', '1y']
base_currency = "ILS"
target_currencies = ["USD", "EUR"]

if stocks:
    data = []
    for ticker in stocks:
        st.write(f"Fetching data for {ticker}...")
        current_price = get_current_stock_price(ticker)
        prices = [get_stock_data(ticker, period).Close.min() for period in periods]
        percentage_differences = calculate_percentage_differences(current_price, prices)
        data.append([ticker, current_price] + percentage_differences)

    df = pd.DataFrame(data, columns=['Ticker', 'Current Price'] + periods)
    st.write(df)

    # Plot heatmap
    fig, ax = plt.subplots()
    sns.heatmap(df.set_index('Ticker').iloc[:, 1:], annot=True, cmap='coolwarm', center=0, ax=ax)
    st.pyplot(fig)

market_status = "open" if is_market_open() else "closed"
st.write(f"The U.S. stock market is currently {market_status}.")
