import axios from "axios";

export const optimizePortfolio = async (riskTolerance: number) => {
  const response = await axios.post("/api/portfolio/optimize", { riskTolerance });
  return response.data;
};