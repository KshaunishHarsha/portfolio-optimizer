from scipy.optimize import minimize
import numpy as np
import pandas as pd
from datetime import datetime
import requests

# Replace with your Alpha Vantage API key
API_KEY = "API_KEY_HERE"
BASE_URL = "https://www.alphavantage.co/query"

# Dummy portfolio with shares, weights, and ESG scores
portfolio = {
    "AAPL": {"shares": 60, "purchase_date": "2023-01-01", "esg_score": 75},
    "TSLA": {"shares": 50, "purchase_date": "2022-06-15", "esg_score": 65},
    "GOOG": {"shares": 80, "purchase_date": "2023-03-20", "esg_score": 80},
    "META": {"shares": 40, "purchase_date": "2021-12-01", "esg_score": 70},
    "NFLX": {"shares": 30, "purchase_date": "2022-11-10", "esg_score": 72},
    "MSFT": {"shares": 70, "purchase_date": "2023-05-05", "esg_score": 85}
}

# Simulated tax rates based on holding period and asset type
def calculate_tax_impact(symbol, purchase_date, sale_date, country_code="US"):
    holding_period = (sale_date - purchase_date).days
    if country_code == "US":
        if holding_period <= 365:  # Short-term capital gains
            return 0.25  # 25% tax rate for short-term gains
        else:  # Long-term capital gains
            return 0.15  # 15% tax rate for long-term gains
    return 0.2  # Default fallback tax rate

# Fetch stock prices (current and historical)
def fetch_stock_price(symbol):
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "1min",
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    try:
        last_refreshed = data["Meta Data"]["3. Last Refreshed"]
        return float(data["Time Series (1min)"][last_refreshed]["1. open"])
    except KeyError:
        return None

def fetch_historical_data(symbol):
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    try:
        time_series = data["Time Series (Daily)"]
        return [float(value["4. close"]) for key, value in time_series.items()]
    except KeyError:
        return None

# Calculate expected returns and covariance
def calculate_expected_returns_and_covariance(portfolio):
    historical_data = {}
    for symbol in portfolio.keys():
        prices = fetch_historical_data(symbol)
        if prices:
            historical_data[symbol] = prices

    returns = {symbol: np.diff(prices) / prices[:-1] for symbol, prices in historical_data.items()}
    returns_matrix = np.array([returns[symbol] for symbol in historical_data.keys()])
    expected_returns = np.mean(returns_matrix, axis=1)
    covariance_matrix = np.cov(returns_matrix)

    return expected_returns, covariance_matrix, list(historical_data.keys())

# Portfolio optimization with ESG integration
def optimize_portfolio(risk_tolerance):
    try:
        expected_returns, covariance_matrix, valid_symbols = calculate_expected_returns_and_covariance(portfolio)
    except ValueError as e:
        print(f"Error: {e}")
        return

    num_assets = len(expected_returns)
    weights = np.ones(num_assets) / num_assets

    # Get the ESG scores for the portfolio
    esg_scores = np.array([portfolio[symbol]["esg_score"] for symbol in valid_symbols])

    def portfolio_performance(weights):
        returns = np.dot(weights, expected_returns)
        risk = np.sqrt(np.dot(weights.T, np.dot(covariance_matrix, weights)))
        return returns, risk

    def tax_adjustment_factor(weights):
        tax_costs = 0
        today = datetime.now().date()
        
        for i, symbol in enumerate(valid_symbols):
            purchase_date = datetime.strptime(portfolio[symbol]["purchase_date"], "%Y-%m-%d").date()
            tax_rate = calculate_tax_impact(symbol, purchase_date, today)
            asset_value = portfolio[symbol]['value'] if 'value' in portfolio[symbol] else 0
            tax_costs += weights[i] * asset_value * tax_rate

        return tax_costs / sum([portfolio[symbol]['value'] for symbol in valid_symbols])

    def esg_penalty_factor(weights):
        # Penalize based on the weighted average ESG score
        weighted_esg_score = np.dot(weights, esg_scores)
        penalty_factor = 100 - weighted_esg_score  # Higher penalty for lower ESG scores
        return penalty_factor

    def objective_function(weights):
        """Objective function to minimize: accounts for return, risk, tax cost, and ESG score."""
        returns, risk = portfolio_performance(weights)
        tax_cost = tax_adjustment_factor(weights)
        esg_penalty = esg_penalty_factor(weights)
        return -returns + risk_tolerance * risk + tax_cost + esg_penalty

    constraints = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1})
    bounds = tuple((0.05, 0.30) for _ in range(num_assets))  # Ensure each asset has a weight between 5% and 30%

    result = minimize(objective_function, weights, method='SLSQP', bounds=bounds, constraints=constraints)

    if result.success:
        optimized_weights = result.x
        print("Optimized Portfolio Weights:")
        for symbol, weight in zip(valid_symbols, optimized_weights):
            print(f"{symbol}: {weight:.2%}")
    else:
        print("Optimization failed:", result.message)

# Update portfolio with current prices
for symbol in portfolio:
    price = fetch_stock_price(symbol)
    if price:
        portfolio[symbol]['price'] = price
        portfolio[symbol]['value'] = portfolio[symbol]['shares'] * price

# Display current portfolio
print("Current Portfolio:")
for symbol, data in portfolio.items():
    print(f"{symbol}: {data['shares']} shares at ${data.get('price', 'N/A')} each, Total Value: ${data.get('value', 'N/A')}")

# Run optimization
risk_tolerance = float(input("Enter your risk tolerance (e.g., 0.05 for low, 0.15 for high): "))
optimize_portfolio(risk_tolerance)

# Example transaction data
transactions = pd.DataFrame({
    'asset': ['AAPL', 'TSLA', 'GOOG'],
    'purchase_date': ['2022-05-01', '2021-07-15', '2020-02-01'],
    'sale_date': ['2024-05-01', '2022-07-15', '2024-02-01']
})

# Convert dates to datetime format
transactions['purchase_date'] = pd.to_datetime(transactions['purchase_date'])
transactions['sale_date'] = pd.to_datetime(transactions['sale_date'])

# Update purchase prices with real-time data
for i, row in transactions.iterrows():
    symbol = row['asset']
    purchase_price = fetch_stock_price(symbol)
    if purchase_price:
        transactions.at[i, 'purchase_price'] = purchase_price

# Accept sale prices from user
for i, row in transactions.iterrows():
    symbol = row['asset']
    sale_price = float(input(f"Enter the sale price for {symbol}: "))
    transactions.at[i, 'sale_price'] = sale_price

# Calculate holding period and classify short-term vs. long-term
transactions['holding_period_days'] = (transactions['sale_date'] - transactions['purchase_date']).dt.days
transactions['capital_gain_type'] = transactions['holding_period_days'].apply(
    lambda x: 'Short-Term' if x < 365 else 'Long-Term'
)

print(transactions[['asset', 'holding_period_days', 'capital_gain_type', 'purchase_price', 'sale_price']])

# Function to estimate tax impact based on simplified rules
def calculate_tax_impact(asset, purchase_price, sale_price, holding_period_days):
    capital_gain = (sale_price - purchase_price) * asset['shares']
    if holding_period_days < 365:
        tax_rate = 0.30  # Short-term capital gains tax rate
    else:
        tax_rate = 0.15  # Long-term capital gains tax rate
    tax_impact = capital_gain * tax_rate
    return tax_impact

# Calculate and display the tax impacts for the portfolio
for i, row in transactions.iterrows():
    symbol = row['asset']
    purchase_price = row['purchase_price']
    sale_price = row['sale_price']
    holding_period_days = row['holding_period_days']
    tax_impact = calculate_tax_impact(portfolio[symbol], purchase_price, sale_price, holding_period_days)
    print(f"Asset: {symbol}")
    print(f"  Purchase Date: {row['purchase_date']}")
    print(f"  Sale Date: {row['sale_date']}")
    print(f"  Purchase Price: ${purchase_price}")
    print(f"  Sale Price: ${sale_price}")
    print(f"  Holding Period: {holding_period_days} days")
    print(f"  Tax Impact: ${tax_impact:.2f}")
    print("\n")
