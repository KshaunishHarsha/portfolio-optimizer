# 📊 Portfolio Optimizer

The **Portfolio Optimizer** is a full-stack web application that helps investors analyze and optimize their stock portfolios in real-time. It integrates a **Python-based financial algorithm** with a modern **React + TypeScript frontend** and a **Node.js backend**, powered by live data from the **Alpha Vantage API**.

---

## 🚀 Features

* 📈 **Real-time Stock Prices** – Fetches live market data using Alpha Vantage.
* ⚖️ **Risk Tolerance Optimization** – Suggests portfolio adjustments based on user-defined risk levels.
* 📊 **Interactive Dashboard** – Visualizes current vs. adjusted holdings with charts.
* 🔄 **Full-Stack Integration** – React (frontend) + Node.js (backend) + Python (algorithm).
* ⚡ **Seamless User Experience** – Clean, responsive UI with instant feedback.

---

## 🛠️ Tech Stack

* **Frontend**: React, TypeScript, TailwindCSS, shadcn/ui, Recharts
* **Backend**: Node.js, Express, TypeScript
* **Algorithm Layer**: Python (NumPy, Requests)
* **API**: [Alpha Vantage](https://www.alphavantage.co/)

---

## 📂 Project Structure

```
portfolio-optimizer/
│── frontend/           # React + TypeScript frontend
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   └── ...
│── backend/            # Node.js + Express backend
│   ├── src/
│   │   ├── controllers/
│   │   ├── routes/
│   │   ├── services/
│   │   └── ...
│   └── portfolio_optimizer.py   # Python algorithm
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/portfolio-optimizer.git
cd portfolio-optimizer
```

### 2️⃣ Backend Setup

```bash
cd backend
npm install
```

* Create a `.env` file in `backend/`:

  ```env
  ALPHA_VANTAGE_API_KEY=your_api_key_here
  PORT=3001
  ```

* Run the backend:

  ```bash
  npm run dev
  ```

### 3️⃣ Frontend Setup

```bash
cd ../frontend
npm install
npm run dev
```

Frontend will run on [http://localhost:3000](http://localhost:3000)
Backend will run on [http://localhost:3001](http://localhost:3001)

---

## 🖥️ Usage

1. Open the frontend in your browser.
2. Enter a **risk tolerance value** (e.g., `0.05` for conservative, `0.15` for aggressive).
3. Click **Optimize Portfolio**.
4. View **current vs. adjusted holdings** and suggested rebalancing.

---

## 📌 Example Screenshot

<img width="1917" height="990" alt="image" src="https://github.com/user-attachments/assets/986d19e3-5f7e-4ff8-8194-b06ec61c1821" />


---

## 📜 License

This project is licensed under the MIT License.

---

✨ Built with React, Node.js, and Python to bring finance and tech together.
