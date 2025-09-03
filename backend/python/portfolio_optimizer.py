import sys
import json
import numpy as np

def optimize_portfolio(risk_tolerance, portfolio_data):
    portfolio = portfolio_data
    total_value = sum(stock["shares"] * stock["price"] for stock in portfolio.values())
    weights = np.array([stock["shares"] * stock["price"] / total_value for stock in portfolio.values()])

    mean_returns = np.random.uniform(0.01, 0.05, len(portfolio))
    cov_matrix = np.random.uniform(0.0001, 0.002, (len(portfolio), len(portfolio)))

    portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
    portfolio_std_dev = np.sqrt(portfolio_variance)

    if risk_tolerance < portfolio_std_dev:
        adjusted_weights = weights * (risk_tolerance / portfolio_std_dev)
        adjusted_weights /= sum(adjusted_weights)
        for i, symbol in enumerate(portfolio.keys()):
            portfolio[symbol]["adjusted_shares"] = int(adjusted_weights[i] * sum(stock["shares"] for stock in portfolio.values()))
    else:
        for symbol in portfolio.keys():
            portfolio[symbol]["adjusted_shares"] = portfolio[symbol]["shares"]

    return portfolio

if __name__ == "__main__":
    risk_tolerance = float(sys.argv[1])
    portfolio_data = json.loads(sys.argv[2])

    optimized_portfolio = optimize_portfolio(risk_tolerance, portfolio_data)
    print(json.dumps(optimized_portfolio))