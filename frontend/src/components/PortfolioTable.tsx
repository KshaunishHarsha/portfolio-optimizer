import React from "react";
import { Portfolio } from "../types/PortfolioTypes";

interface Props {
  portfolio: Portfolio;
}

const PortfolioTable: React.FC<Props> = ({ portfolio }) => {
  if (!Object.keys(portfolio).length) {
    return (
      <p className="text-center text-muted">No portfolio data available.</p>
    );
  }

  return (
    <table className="table table-bordered table-striped table-hover">
      <thead className="table-dark">
        <tr>
          <th>Symbol</th>
          <th>Shares</th>
          <th>Price</th>
          <th>Value</th>
          <th>Adjusted Shares</th>
        </tr>
      </thead>
      <tbody>
        {Object.entries(portfolio).map(([symbol, data]) => (
          <tr key={symbol}>
            <td>{symbol}</td>
            <td>{data.shares}</td>
            <td>{data.price?.toFixed(2) || "N/A"}</td>
            <td>{(data.shares * (data.price || 0)).toFixed(2) || "N/A"}</td>
            <td>{data.adjusted_shares || data.shares}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default PortfolioTable;
