import pandas as pd
import yfinance as yf
import numpy as np
import time
from nasdaq import market_overview
from webhook import send_message, send_discord_alert
import logging


def get_stock_data(ticker):
    """
    Fetches historical stock data from Yahoo Finance
    """
    
    start_date = '2024-01-01'
    end_date = int(time.time())
    
    try:
        # Fetch data
        data = yf.download(ticker, start=start_date, end=end_date)
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_rsi(data, window=14):
    """
    Calculates Relative Strength Index (RSI) for given stock data
    """
    try:
        # Calculate price changes
        delta = data['Close'].diff()

        # Get gains and losses
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        # Compute average gain/loss
        avg_gain = gain.ewm(com=window - 1, min_periods=window).mean()
        avg_loss = loss.ewm(com=window - 1, min_periods=window).mean()

        # Calculate RS
        rs = avg_gain / (avg_loss + np.finfo(float).eps)  # Adding epsilon to avoid division by zero

        # Calculate RSI
        rsi = 100 - (100 / (1 + rs))

        return rsi
    except Exception as e:
        print(f"Error calculating RSI: {e}")
        return None

def calculate_current_rsi(data, window=14):
    """
    Calculates the current Relative Strength Index (RSI) for given stock data
    """
    all = calculate_rsi(data, window)
    return all.iloc[-1].item()


# Example usage:
if __name__ == "__main__":
    # Fetch Apple stock data from last year to today
    ticker = 'AVGO'
    companies = market_overview()
    # setting up logger
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename=f'logs/{time.time()}.log', encoding='utf-8', level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler())

    for company in companies:
        time.sleep(1)
        try:
            market_cap = float(company['marketCap'])
            if(market_cap < 10_000_000_000): # Skip companies with small market cap
                continue
            ticker = company['symbol']
            name = company['name']
            logger.info(f"Fetching data for {name} ({ticker})")
            data = get_stock_data(ticker)
            if data is None:
                logger.error("No data available for {name} ({ticker})")
                continue
            current_rsi = calculate_current_rsi(data)
            logger.info(f"RSI for {name} ({ticker}): {current_rsi}")
            if current_rsi < 20:
                logger.info(f"BUY {name} ({ticker})")
                send_discord_alert(company, current_rsi)
            elif current_rsi > 80:
                logger.info(f"SELL {name} ({ticker})")

        except Exception as e:
            logger.error(f"Error processing data for {name} ({ticker}): {e}")
        
        time.sleep(10)  # Sleep to avoid rate limiting
    
    logger.info("Done processing all companies")