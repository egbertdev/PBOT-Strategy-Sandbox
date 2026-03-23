# Quantitative Strategy Sandbox (PBOT)
### **High-Frequency Statistical Execution Engine**

[**Watch Technical Demo**](INSERT_YOUTUBE_LINK_HERE) | [**Portfolio**](https://egbert-joel.vercel.app/)

## **Project Overview**
PBOT is a headless execution engine developed to stress-test high-frequency statistical strategies (Martingale, Trend-Following, and Mean Reversion) against real-time WebSocket-driven data. It transitions manual trading concepts into a programmatic, emotionless execution environment.

## **The Logic**
Designed with a "Mechanical Engineering" approach to risk, the system prioritizes **Systemic Gating**. Instead of constant execution, the engine remains idle until specific statistical "exhaustion" thresholds are met, significantly increasing the probability of successful entries.

## **Technical Architecture**
* **Language:** Python 3.x
* **Automation Engine:** Selenium (Optimized for sub-100ms latency)
* **GUI Framework:** Tkinter (Custom dashboard for real-time parameter tuning)
* **Data Parsing:** BeautifulSoup4 & JSON Normalization
* **Real-Time Monitoring:** Custom `WebDriverWait` logic for WebSocket event tracking

## **Key Features**
* **Conditional Gating Algorithm:** Implements "Programmatic Patience"—executing only when specific trend-exhaustion criteria (e.g., consecutive loss streaks) are met.
* **Real-Time Risk Management:** Automated stop-loss triggers and stake-sequencing based on live balance fluctuations.
* **State-Machine Architecture:** Robust session persistence and error-handling to manage network volatility and authentication.
* **Live Dashboard:** A custom-built Tkinter interface allows the user to adjust risk parameters (Stake, Thresholds, Target ROI) on the fly.

## **Installation & Setup**

```bash
git clone [https://github.com/egbertdev/PBOT-Strategy-Sandbox.git](https://github.com/egbertdev/PBOT-Strategy-Sandbox.git)
cd PBOT-Strategy-Sandbox
2. Install Dependencies
Bash
pip install selenium beautifulsoup4
3. Run the Engine
Bash
python main.py
Author: Egbert Joel Abok

Focus: Quantitative Automation & Systems Logic
