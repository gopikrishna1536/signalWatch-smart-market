# SignalWatch — Smart Market Quantitative Analysis Engine

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Testing](https://img.shields.io/badge/Tests-100%25%20Passing-25A162?style=for-the-badge)](tests/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

A high-performance Python quantitative finance engine designed to compute technical indicators, detect market regime transitions, and generate algorithmic trading signals (moving average crossovers, RSI mean reversion, and Bollinger Band breakouts) exposed via a modern FastAPI REST service.

---

## 📈 Technical Indicators & Algorithms

1. **Simple Moving Average (SMA):**
   $$SMA_t = \frac{1}{n} \sum_{i=0}^{n-1} P_{t-i}$$
2. **Exponential Moving Average (EMA):**
   $$EMA_t = (P_t - EMA_{t-1}) \times \left(\frac{2}{n + 1}\right) + EMA_{t-1}$$
3. **Relative Strength Index (RSI):**
   $$RSI = 100 - \left(\frac{100}{1 + RS}\right) \quad \text{where} \quad RS = \frac{\text{Smoothed Avg Gain}}{\text{Smoothed Avg Loss}}$$
   - **Overbought Condition ($RSI \ge 70$):** Signals profit-taking or short opportunities.
   - **Oversold Condition ($RSI \le 30$):** Signals mean-reversion buying opportunities.
4. **Bollinger Bands:**
   - Middle Band = $SMA(20)$
   - Upper Band = $SMA(20) + 2\sigma$
   - Lower Band = $SMA(20) - 2\sigma$
5. **Moving Average Crossovers:**
   - **Golden Cross:** Fast moving average breaks strictly above slow moving average (bullish reversal).
   - **Death Cross:** Fast moving average breaks strictly below slow moving average (bearish breakdown).

---

## 🏛️ Architecture & Project Structure

```
signalWatch-smart-market/
├── .github/
│   └── workflows/
│       └── python-ci.yml           # Automated GitHub Actions test pipeline
├── signalwatch/
│   ├── __init__.py
│   ├── api.py                      # FastAPI REST endpoints & Swagger documentation
│   ├── indicators.py               # Pure Python mathematical indicator calculations
│   └── signals.py                  # Quantitative signal generation & crossover detection
├── tests/
│   ├── __init__.py
│   └── test_signalwatch.py         # Automated unit test suite
├── Dockerfile                      # Production container image
├── docker-compose.yml              # Multi-container orchestration
├── requirements.txt                # Python dependencies
├── .gitignore                      # Python git ignore rules
└── README.md                       # Documentation
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- Optional: Docker & Docker Compose

### Option A: Running with Docker Compose (Recommended)

```bash
docker-compose up -d --build
```

Access interactive Swagger documentation at:  
👉 **`http://localhost:8000/docs`**

---

### Option B: Local Execution

1. **Clone the repository:**
   ```bash
   git clone https://github.com/gopikrishna1536/signalWatch-smart-market.git
   cd signalWatch-smart-market
   ```

2. **Run automated unit tests:**
   ```bash
   python -m unittest discover tests
   ```

3. **Install dependencies and launch FastAPI:**
   ```bash
   pip install -r requirements.txt
   uvicorn signalwatch.api:app --reload --port 8000
   ```

---

## 🧪 Automated Testing

Unit tests run with standard library `unittest` and `pytest`:
- Mathematical accuracy of Simple & Exponential Moving Averages
- RSI bounding ($0 \le RSI \le 100$) and Wilder's smoothing verification
- Bollinger Band structural ordering ($\text{Upper} > \text{Middle} > \text{Lower}$)
- Golden Cross and Death Cross trigger validation

Run tests:
```bash
python -m unittest discover tests
```

---

## 📄 License
MIT License.
