import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.table as tbl

"""
    @Brief: Fetches historical stock data in pd DataFrame

    @Args:
        ticker (string): The stock ticker symbol (e.g., 'INFY').
        period (string): The time period for historical data (e.g., '1y')

    @Returns:
        pd.DataFrame: DataFrame- 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends'.
        yf.Ticker: yfinance Ticker object for additional stock information and methods.
"""
def fetch_stock_data(ticker, period="1y"):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data, stock

"""
    @Brief: Calculates key financial metrics from historical stock price data.

    @Args:
        data (pd.DataFrame): DataFrame containing historical stock data with at least 'Close' prices.

    @Returns:
        pd.DataFrame: DataFrame containing calculated metrics:
            - 'daily_return': Daily percentage change in closing prices.
            - 'cumulative_return': Cumulative return over the period.
            - 'moving_average_50': 50-day moving average of closing prices.
            - 'moving_average_200': 200-day moving average of closing prices.
            - 'volatility': 30-day rolling volatility (annualized).
            - 'sharpe_ratio': Annualized Sharpe ratio.
            - 'bollinger_upper': Upper Bollinger Band.
            - 'bollinger_lower': Lower Bollinger Band.
"""
def calculate_financial_metrics(data):
    metrics = {}
    metrics['daily_return'] = data['Close'].pct_change()
    metrics['cumulative_return'] = (1 + metrics['daily_return']).cumprod() - 1
    metrics['moving_average_50'] = data['Close'].rolling(window=50).mean()
    metrics['moving_average_200'] = data['Close'].rolling(window=200).mean()
    metrics['volatility'] = metrics['daily_return'].rolling(window=30).std() * np.sqrt(252)
    metrics['sharpe_ratio'] = (metrics['daily_return'].mean() / metrics['daily_return'].std()) * np.sqrt(252)
    metrics['bollinger_upper'] = metrics['moving_average_50'] + 2 * metrics['volatility']
    metrics['bollinger_lower'] = metrics['moving_average_50'] - 2 * metrics['volatility']
    
    return pd.DataFrame(metrics)

"""
    @Brief: Extracts and formats additional financial ratios from the stock metadata.

    @Args:
        stock (yf.Ticker): yfinance Ticker object for the stock.

    @Returns:
        dict: Dictionary containing additional financial ratios:
            - 'PE Ratio': Price-to-Earnings ratio (trailing P/E).
            - 'PB Ratio': Price-to-Book ratio.
            - 'Dividend Yield': Dividend yield percentage.
            - 'EPS': Earnings Per Share (trailing EPS).
            - 'Market Cap': Market capitalization formatted with commas (if available), otherwise 'N/A'.
"""
def calculate_additional_financial_ratios(stock):
    ratios = {}
    info = stock.info
    ratios['PE Ratio'] = info.get('trailingPE', 'N/A')
    ratios['PB Ratio'] = info.get('priceToBook', 'N/A')
    ratios['Dividend Yield'] = info.get('dividendYield', 'N/A')
    ratios['EPS'] = info.get('trailingEps', 'N/A')
    ratios['Market Cap'] = info.get('marketCap')
    if isinstance(ratios['Market Cap'], (int, float)):
        ratios['Market Cap'] = f"{int(ratios['Market Cap']):,}"
    else:
        ratios['Market Cap'] = 'N/A'
    return ratios

# Redundant As of Now! Since, We'll be pd Tables an Images to Output the Data related to a Stock! 
def generate_report(ticker, metrics, ratios, stock):
    report = f"""
    Stock Report for {ticker.upper()} - Generated on {datetime.now().strftime('%Y-%m-%d')}
    ================================================================================
    
    1. Stock Overview:
    - Name: {stock.info['longName']}
    - Ticker: {ticker.upper()}
    - Market Cap: {ratios['Market Cap']}
    - P/E Ratio: {ratios['PE Ratio']}
    - P/B Ratio: {ratios['PB Ratio']}
    - EPS: {ratios['EPS']}
    - Dividend Yield: {ratios['Dividend Yield']}

    2. Key Financial Metrics:
    - 1-Year Cumulative Return: {metrics['cumulative_return'].iloc[-1]:.2%}
    - Volatility (30-Day): {metrics['volatility'].iloc[-1]:.2%}
    - Sharpe Ratio: {metrics['sharpe_ratio'].iloc[-1]:.2f}

    3. Moving Averages: 
    - 50-Day Moving Average: ${metrics['moving_average_50'].iloc[-1]:.2f}
    - 200-Day Moving Average: ${metrics['moving_average_200'].iloc[-1]:.2f}

    4. Bollinger Bands: 
    - Upper Band: ${metrics['bollinger_upper'].iloc[-1]:.2f}
    - Lower Band: ${metrics['bollinger_lower'].iloc[-1]:.2f}

    5. Technical Indicators:
    - The stock is {('above' if metrics['moving_average_50'].iloc[-1] > metrics['moving_average_200'].iloc[-1] else 'below')} the 200-Day Moving Average, indicating a {('bullish' if metrics['moving_average_50'].iloc[-1] > metrics['moving_average_200'].iloc[-1] else 'bearish')} trend.
    - The stock is {('above' if stock.history(period='1d')['Close'].iloc[-1] > metrics['bollinger_upper'].iloc[-1] else 'below' if stock.history(period='1d')['Close'].iloc[-1] < metrics['bollinger_lower'].iloc[-1] else 'within')} the Bollinger Bands.

    ================================================================================
    """
    
    return report

def save_table_image(ticker, metrics, ratios):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('off')

    # Combine metrics and ratios into a table
    table_data = [
        ["Metric", "Value"],
        ["Market Cap", ratios['Market Cap']],
        ["P/E Ratio", ratios['PE Ratio']],
        ["P/B Ratio", ratios['PB Ratio']],
        ["EPS", ratios['EPS']],
        ["Dividend Yield", ratios['Dividend Yield']],
        ["1-Year Cumulative Return", f"{metrics['cumulative_return'].iloc[-1]:.2%}"],
        ["Volatility (30-Day)", f"{metrics['volatility'].iloc[-1]:.2%}"],
        ["Sharpe Ratio", f"{metrics['sharpe_ratio'].iloc[-1]:.2f}"],
        ["50-Day Moving Average", f"${metrics['moving_average_50'].iloc[-1]:.2f}"],
        ["200-Day Moving Average", f"${metrics['moving_average_200'].iloc[-1]:.2f}"],
        ["Bollinger Upper Band", f"${metrics['bollinger_upper'].iloc[-1]:.2f}"],
        ["Bollinger Lower Band", f"${metrics['bollinger_lower'].iloc[-1]:.2f}"]
    ]

    table = ax.table(cellText=table_data, colLabels=None, cellLoc='left', loc='center', bbox=[0, 0, 1, 1])

    # Style the table
    for (i, j), cell in table._cells.items():
        if i == 0:  # Heading row
            cell.set_text_props(fontweight='bold', fontsize=12)
            cell.set_facecolor('lightgray')
        else:
            cell.set_text_props(fontsize=10)

    table.auto_set_font_size(False)
    table.scale(1.2, 1.2)
    plt.title(f'{ticker.upper()} Financial Metrics')

    plt.savefig(f'{ticker.upper()}_Metrics_Table.png', bbox_inches='tight')
    plt.close()

def plot_metrics(ticker, data, metrics):
    plt.figure(figsize=(14, 7))
    plt.plot(data.index, data['Close'], label='Close Price', color='black')
    plt.plot(metrics.index, metrics['moving_average_50'], label='50-Day MA', color='blue', linestyle='--')
    plt.plot(metrics.index, metrics['moving_average_200'], label='200-Day MA', color='red', linestyle='--')
    plt.fill_between(metrics.index, metrics['bollinger_upper'], metrics['bollinger_lower'], color='gray', alpha=0.3, label='Bollinger Bands')
    
    plt.title(f'{ticker.upper()} Price and Technical Indicators')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend(loc='upper left')
    plt.grid(True)
    
    plt.savefig(f'{ticker.upper()}_Technical_Indicators.png', bbox_inches='tight')
    plt.close()

def main(ticker, save=False):
    data, stock = fetch_stock_data(ticker)
    metrics = calculate_financial_metrics(data)
    ratios = calculate_additional_financial_ratios(stock)
    report = generate_report(ticker, metrics, ratios, stock)
    if save:
        save_table_image(ticker, metrics, ratios)
        plot_metrics(ticker, data, metrics)
    else:
        print("Saving Not Required!")
    print(report)

if __name__ == "__main__":
    ticker = input("Enter the stock ticker (e.g., AAPL): ")
    ticker.strip().upper()
    main(ticker=ticker, save=True)
