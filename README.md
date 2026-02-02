# Auto Trade Tool Pro v1.0 – Real-Time Trading Signals & Backtesting Dashboard (Full Source Code)

**Auto Trade Tool Pro v1.0** is a Python web application built with **Streamlit** for **automated trade signal generation, risk management, backtesting, and Telegram notifications**.  
This repository contains the full source code, allowing you to customize **signal logic, indicators, risk/reward calculations, session management, and UI components** for personal, learning, or professional trading analysis.

------------------------------------------------------------
🌟 FEATURES
------------------------------------------------------------

- 📈 Multi-Market Support — BTC/USDT, EUR/USD, USD/JPY, S&P500  
- ⏱ Multiple Timeframes — Scalping (5m), Intraday (15m), Swing (1h)  
- 💹 Indicators — EMA20, EMA50, ATR (Average True Range)  
- ⚖ Risk Management — Automatic lot size calculation based on account balance and stop loss  
- 🎯 Signal Generation — BUY / SELL signals with Entry, Stop Loss, Take Profit  
- 🔁 Backtesting — Calculate historical win rate based on EMA strategy  
- 📲 Telegram Integration — Send signals directly to your bot or group  
- 🖥 Real-Time Market Data — Fetch last 14 days of OHLC data via Yahoo Finance  
- 🧮 Adjustable Risk/Reward — Slider for Risk:Reward ratio and Risk % per trade  
- 🌐 Session Detection — Automatically identifies Asia, London, or New York sessions  
- 📊 Interactive Charts — Line chart of Close price, EMA20, and EMA50  
- 🗂 Recent Market Data — Expandable table for last 20 candles  

------------------------------------------------------------
🚀 INSTALLATION
------------------------------------------------------------

1. Clone or download this repository:

```
git clone https://github.com/rogers-cyber/AutoTradeToolPro.git
cd AutoTradeToolPro
```

2. Install required Python packages:

```
pip install streamlit yfinance pandas ta numpy requests
```

3. Run the application:

```
streamlit run app.py
```

------------------------------------------------------------
💡 USAGE
------------------------------------------------------------

1. Select Market & Mode:
   - Choose your trading symbol (BTCUSDT, EURUSD, USDJPY, US500)  
   - Choose timeframe (Scalping, Intraday, Swing)  

2. Configure Risk:
   - Set **Risk:Reward ratio**  
   - Set **Risk %** of account per trade  
   - Enter **Account Balance**  

3. Telegram Setup (Optional):
   - Enter your **Bot Token** and **Chat ID**  
   - Test connection to ensure messages can be sent  

4. Generate Signal:
   - Click **Generate Signal**  
   - View **Signal, Entry, SL, TP, Lot Size, and Win Rate**  
   - Signals automatically sent via Telegram if configured  

5. Review Charts & Data:
   - Inspect **line chart** with Close, EMA20, and EMA50  
   - Expand **Recent Market Data** table for the last 20 candles  

------------------------------------------------------------
⚙️ CONFIGURATION OPTIONS
------------------------------------------------------------

Option                   | Description
------------------------ | --------------------------------------------------
Market                   | Select symbol (BTCUSDT, EURUSD, USDJPY, US500)  
Mode                     | Select timeframe (Scalping, Intraday, Swing)  
Risk:Reward              | Ratio of Take Profit vs Stop Loss  
Risk %                   | Percentage of balance risked per trade  
Account Balance           | Used to calculate lot size  
Telegram Token & Chat ID  | For sending signals automatically  
Win Rate Calculation      | Historical EMA crossover backtest  
Chart                     | Visualize price and EMA indicators  
Recent Data Table         | View OHLC and indicator values  

------------------------------------------------------------
📦 OUTPUT
------------------------------------------------------------

- Trade Signal — BUY / SELL with Entry, SL, TP  
- Lot Size — Calculated based on risk management  
- Win Rate — EMA crossover backtest percentage  
- Telegram Notification — Optional real-time signal alerts  
- Charts & Data — Streamlit-rendered visualizations  

------------------------------------------------------------
📦 DEPENDENCIES
------------------------------------------------------------

- Python 3.10+  
- Streamlit — Web app framework  
- yfinance — Market data fetching  
- pandas — Data manipulation  
- ta — Technical analysis indicators  
- numpy — Numeric operations  
- requests — Telegram API communication  

------------------------------------------------------------
📝 NOTES
------------------------------------------------------------

- Fully online: requires internet to fetch Yahoo Finance data  
- EMA20 / EMA50 crossover strategy used for signals and backtesting  
- ATR-based Stop Loss and Take Profit for dynamic trade management  
- Lot size calculated automatically based on account balance and risk %  
- Session detection adjusts info based on Asia, London, or New York market times  

------------------------------------------------------------
👤 ABOUT
------------------------------------------------------------

**Auto Trade Tool Pro v1.0** is maintained by **Mate Technologies**, providing a **real-time trading signal generator and backtesting dashboard** for educational and trading analysis purposes.

Website / Contact: https://github.com/rogers-cyber

------------------------------------------------------------
📜 LICENSE
------------------------------------------------------------

Distributed as source code.  
You may use it for personal or educational projects.  
Redistribution, resale, or commercial use requires explicit permission.
