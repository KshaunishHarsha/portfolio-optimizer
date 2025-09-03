import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import pandas as pd
from datetime import datetime
import requests

# Replace with your Alpha Vantage API key
API_KEY = "RE6JH1LH4ZYD75ZB"
BASE_URL = "https://www.alphavantage.co/query"

# Dummy portfolio with shares and weights
portfolio = {
    "AAPL": {"shares": 60, "purchase_date": "2023-01-01"},
    "TSLA": {"shares": 50, "purchase_date": "2022-06-15"},
    "GOOG": {"shares": 80, "purchase_date": "2023-03-20"},
    "META": {"shares": 40, "purchase_date": "2021-12-01"},
    "NFLX": {"shares": 30, "purchase_date": "2022-11-10"},
    "MSFT": {"shares": 70, "purchase_date": "2023-05-05"}
}

# Fetch stock prices (current and historical)
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

# Portfolio optimization
def optimize_portfolio(risk_tolerance, expected_returns, covariance_matrix):
    num_assets = len(expected_returns)
    weights = np.ones(num_assets) / num_assets

    def portfolio_performance(weights):
        returns = np.dot(weights, expected_returns)
        risk = np.sqrt(np.dot(weights.T, np.dot(covariance_matrix, weights)))
        return returns, risk

    def objective_function(weights):
        returns, risk = portfolio_performance(weights)
        return -returns + risk_tolerance * risk

    constraints = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1})
    bounds = tuple((0.05, 0.30) for _ in range(num_assets))

    result = minimize(objective_function, weights, method='SLSQP', bounds=bounds, constraints=constraints)

    if result.success:
        optimized_weights = result.x
        return optimized_weights
    else:
        print("Optimization failed:", result.message)
        return None

# Get current portfolio return and risk
def current_portfolio_performance(expected_returns, covariance_matrix, portfolio):
    valid_symbols = list(portfolio.keys())
    weights = np.array([portfolio[symbol]["shares"] / sum([data["shares"] for data in portfolio.values()]) for symbol in valid_symbols])
    returns = np.dot(weights, expected_returns)
    risk = np.sqrt(np.dot(weights.T, np.dot(covariance_matrix, weights)))
    return returns, risk

# Update portfolio with current prices
for symbol in portfolio:
    price = fetch_historical_data(symbol)[-1]  # Get the latest price
    portfolio[symbol]['price'] = price
    portfolio[symbol]['value'] = portfolio[symbol]['shares'] * price

# Calculate expected returns and covariance matrix
expected_returns, covariance_matrix, valid_symbols = calculate_expected_returns_and_covariance(portfolio)

# Get current portfolio performance
current_return, current_risk = current_portfolio_performance(expected_returns, covariance_matrix, portfolio)

# Run optimization with user-defined risk tolerance
risk_tolerance = float(input("Enter your risk tolerance (e.g., 0.05 for low, 0.15 for high): "))
optimized_weights = optimize_portfolio(risk_tolerance, expected_returns, covariance_matrix)

# Calculate optimized portfolio performance
if optimized_weights is not None:
    optimized_return = np.dot(optimized_weights, expected_returns)
    optimized_risk = np.sqrt(np.dot(optimized_weights.T, np.dot(covariance_matrix, optimized_weights)))
else:
    optimized_return, optimized_risk = None, None

# Plot graphs for current vs optimized portfolio performance
plt.figure(figsize=(12, 6))

# Scatter plot for current and optimized portfolio
plt.subplot(1, 2, 1)
plt.scatter(current_risk, current_return, color='red', label='Current Portfolio', s=100)
if optimized_return is not None:
    plt.scatter(optimized_risk, optimized_return, color='green', label='Optimized Portfolio', s=100)
plt.title('Risk-Return for Current vs Optimized Portfolio')
plt.xlabel('Risk (Standard Deviation)')
plt.ylabel('Expected Return')
plt.legend()

# Plotting Efficient Frontier (for illustration)
# Generate random portfolios for illustration
num_portfolios = 10000
results = np.zeros((3, num_portfolios))
for i in range(num_portfolios):
    weights = np.random.random(len(expected_returns))
    weights /= np.sum(weights)
    portfolio_return, portfolio_risk = np.dot(weights, expected_returns), np.sqrt(np.dot(weights.T, np.dot(covariance_matrix, weights)))
    results[0, i] = portfolio_return
    results[1, i] = portfolio_risk
    results[2, i] = results[0, i] / results[1, i]  # Sharpe ratio

plt.subplot(1, 2, 2)
plt.scatter(results[1, :], results[0, :], c=results[2, :], cmap='YlGnBu', marker='o')
plt.colorbar(label='Sharpe Ratio')
plt.title('Efficient Frontier')
plt.xlabel('Risk (Standard Deviation)')
plt.ylabel('Expected Return')

plt.tight_layout()
plt.show()