import React, { useState } from "react";
import PortfolioTable from "./components/PortfolioTable";
import { optimizePortfolio } from "./services/api";
import { Portfolio } from "./types/PortfolioTypes";
import { FaChartLine, FaSyncAlt } from "react-icons/fa";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const App: React.FC = () => {
  const [portfolio, setPortfolio] = useState<Portfolio>({});
  const [riskTolerance, setRiskTolerance] = useState<number>(0.02);
  const [loading, setLoading] = useState(false);

  const handleOptimize = async () => {
    setLoading(true);
    try {
      const result = await optimizePortfolio(riskTolerance);
      setPortfolio(result);
      toast.success("Portfolio optimized successfully!");
    } catch (error) {
      toast.error("Failed to optimize portfolio.");
    }
    setLoading(false);
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "linear-gradient(135deg, #e0e7ff 0%, #f8fafc 100%)",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        width: "100vw", // Ensure full viewport width
        margin: "0 auto", // Horizontally center the div
      }}
    >
      <ToastContainer position="top-center" />
      <header
        className="py-5 mb-4"
        style={{
          background: "linear-gradient(90deg, #6366f1 0%, #60a5fa 100%)",
          color: "#fff",
          borderRadius: "0 0 2rem 2rem",
          boxShadow: "0 4px 24px rgba(99,102,241,0.15)",
          width: "100%",
          textAlign: "center",
        }}
      >
        <div className="container text-center">
          <FaChartLine size={48} className="mb-2" />
          <h1 className="fw-bold mb-0">Portfolio Optimizer</h1>
          <p className="lead mb-0">Maximize returns, minimize risk.</p>
        </div>
      </header>
      <div
        className="container d-flex flex-column align-items-center"
        style={{ width: "100%", maxWidth: 600 }}
      >
        <div
          className="card p-4 mb-4 shadow-sm"
          style={{
            borderRadius: "1.5rem",
            width: "100%",
            display: "flex",
            alignItems: "center",
          }}
        >
          <div className="mb-3 w-100" style={{ textAlign: "center" }}>
            <label htmlFor="riskTolerance" className="form-label fw-semibold">
              Risk Tolerance
            </label>
            <div
              className="input-group justify-content-center"
              style={{ width: "60%", margin: "0 auto" }}
            >
              <span className="input-group-text">
                <FaChartLine />
              </span>
              <input
                type="number"
                id="riskTolerance"
                className="form-control text-center"
                value={riskTolerance}
                onChange={(e) => setRiskTolerance(parseFloat(e.target.value))}
                step="0.01"
                min="0.01"
              />
            </div>
            <div className="form-text">
              Set your acceptable risk level (e.g., 0.01 = low risk, 0.10 = high
              risk)
            </div>
          </div>
          <button
            className="btn btn-primary w-75 d-flex align-items-center justify-content-center gap-2"
            onClick={handleOptimize}
            disabled={loading}
            style={{
              fontWeight: 600,
              fontSize: "1.1rem",
              borderRadius: "0.75rem",
              margin: "0 auto",
            }}
          >
            {loading ? (
              <>
                <FaSyncAlt className="fa-spin" /> Optimizing...
              </>
            ) : (
              <>
                <FaSyncAlt /> Optimize Portfolio
              </>
            )}
          </button>
        </div>
        <div
          style={{ width: "100%", display: "flex", justifyContent: "center" }}
        >
          <PortfolioTable portfolio={portfolio} />
        </div>
      </div>
    </div>
  );
};

export default App;
