const express = require("express");
const { execFile } = require("child_process");
const path = require("path");

const router = express.Router();

const portfolio = {
  AAPL: { shares: 60, price: 150 },
  TSLA: { shares: 50, price: 700 },
  GOOG: { shares: 80, price: 2800 },
  META: { shares: 40, price: 350 },
  NFLX: { shares: 30, price: 600 },
  MSFT: { shares: 70, price: 320 },
};

// Call the Python script
function optimizePortfolio(riskTolerance, portfolioData) {
  return new Promise((resolve, reject) => {
    const pythonScript = path.join(__dirname, "../../python/portfolio_optimizer.py");
    const args = [riskTolerance, JSON.stringify(portfolioData)];

    execFile("python", [pythonScript, ...args], (error, stdout, stderr) => {
      if (error) {
        return reject(error);
      }
      if (stderr) {
        return reject(stderr);
      }
      resolve(JSON.parse(stdout));
    });
  });
}

// API endpoint
router.post("/optimize", async (req, res) => {
  try {
    const { riskTolerance } = req.body;
    const optimizedPortfolio = await optimizePortfolio(riskTolerance, portfolio);
    res.json(optimizedPortfolio);
  } catch (error) {
    console.error("Optimization error:", error);
    res.status(500).json({ error: "Failed to optimize portfolio" });
  }
});

module.exports = router;