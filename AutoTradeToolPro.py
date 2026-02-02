import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import numpy as np
import requests
from datetime import datetime, time

# ---------------- PAGE ----------------
st.set_page_config(page_title="Auto Trade Tool Pro", layout="wide")
st.title("🚀 Auto Trade Tool Pro")

# ---------------- SYMBOLS ----------------
SYMBOLS = {
    "BTCUSDT": "BTC-USD",
    "EURUSD": "EURUSD=X",
    "USDJPY": "JPY=X",
    "US500": "^GSPC",
}

TIMEFRAMES = {
    "Scalping": "5m",
    "Intraday": "15m",
    "Swing": "1h",
}

MODE_SETTINGS = {
    "Scalping": 1.0,
    "Intraday": 1.5,
    "Swing": 2.0,
}

# ---------------- SESSION ----------------
def current_session():
    utc = datetime.utcnow().time()
    if time(0,0) <= utc <= time(7,59):
        return "Asia"
    elif time(8,0) <= utc <= time(15,59):
        return "London"
    else:
        return "New York"

# ---------------- TELEGRAM ----------------
def send_telegram(msg, token, chat_id):
    if token == "" or chat_id == "":
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, data={"chat_id": chat_id, "text": msg})
    except:
        pass

# ---------------- LOT SIZE ----------------
def lot_size(balance, risk_pct, entry, sl):
    risk_amount = balance * (risk_pct / 100)
    stop = abs(entry - sl)
    if stop == 0:
        return 0
    return round(risk_amount / stop, 2)

# ---------------- BACKTEST ----------------
def backtest(df):
    wins = 0
    losses = 0

    for i in range(50, len(df)-1):
        row = df.iloc[i]
        nxt = df.iloc[i+1]

        # Ensure numeric comparison
        ema20 = float(row["ema20"])
        ema50 = float(row["ema50"])
        close_now = float(row["Close"])
        close_next = float(nxt["Close"])

        if ema20 > ema50:
            if close_next > close_now:
                wins += 1
            else:
                losses += 1
        else:
            if close_next < close_now:
                wins += 1
            else:
                losses += 1

    total = wins + losses
    if total == 0:
        return 0
    return round(wins / total * 100, 2)

# ---------------- TELEGRAM INPUT ----------------
with st.expander("📲 Telegram Settings (Per User)"):
    if "tg_token" not in st.session_state:
        st.session_state.tg_token = ""
    if "tg_chat" not in st.session_state:
        st.session_state.tg_chat = ""

    TELEGRAM_TOKEN = st.text_input(
        "Telegram Bot Token", 
        type="password", 
        key="tg_token",
        help="Enter your Bot Token from @BotFather. Keep it secret!"
    )

    TELEGRAM_CHAT_ID = st.text_input(
        "Telegram Chat ID", 
        key="tg_chat",
        help="Enter your Chat ID where signals will be sent. Can be your private chat ID or a group ID."
    )

    if st.button("Show Telegram Setup Guide"):
        st.markdown("""
        **Step 1:** Create a bot via @BotFather and get the token.  
        **Step 2:** Open a chat with your bot or a group and send a message.  
        **Step 3:** Go to `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`  
        **Step 4:** Find `"chat" → "id"` in the JSON response.  
        **Step 5:** Copy that number into the Telegram Chat ID field above.
        """)

    if st.button("Test Telegram Connection"):
        if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
            send_telegram("✅ Test message from Auto Trade Tool Pro", TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)
            st.success("Test message sent! Check your Telegram.")
        else:
            st.warning("Please fill both Bot Token and Chat ID first.")

# ---------------- CONTROLS ----------------
c1, c2, c3, c4 = st.columns(4)
symbol = c1.selectbox("Market", SYMBOLS.keys())
mode = c2.selectbox("Mode", TIMEFRAMES.keys())
risk_reward = c3.slider("Risk : Reward", 1.0, 5.0, 2.0, 0.5)
risk_pct = c4.slider("Risk %", 0.5, 5.0, 1.0, 0.5)
balance = st.number_input("Account Balance", value=1000.0)

st.info(f"Current Trading Session: {current_session()}")

timeframe = TIMEFRAMES[mode]
atr_mult = MODE_SETTINGS[mode]

# ---------------- MAIN ----------------
if st.button("Generate Signal"):

    # Download data
    df = yf.download(
        SYMBOLS[symbol],
        period="14d",
        interval=timeframe,
        group_by="column",
        progress=False
    )

    if df.empty:
        st.error("Failed to download data. Try a different symbol or timeframe.")
        st.stop()

    # ---------------- MULTIINDEX FIX ----------------
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]

    # Ensure all OHLC columns are numeric
    for col in ["Open","High","Low","Close"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df.dropna(inplace=True)

    # ---------------- INDICATORS ----------------
    close = pd.Series(df["Close"].values.flatten(), index=df.index)
    high = pd.Series(df["High"].values.flatten(), index=df.index)
    low = pd.Series(df["Low"].values.flatten(), index=df.index)

    df["ema20"] = ta.trend.ema_indicator(close, window=20).astype(float)
    df["ema50"] = ta.trend.ema_indicator(close, window=50).astype(float)
    df["atr"] = ta.volatility.average_true_range(high, low, close, window=14).astype(float)

    # ---------------- LAST CANDLE ----------------
    last = df.iloc[-1]
    price = float(last["Close"])
    atr = float(last["atr"]) * atr_mult
    ema20_val = float(last["ema20"])
    ema50_val = float(last["ema50"])

    if ema20_val > ema50_val:
        direction = "BUY"
        entry = price
        sl = entry - atr
        tp = entry + atr * risk_reward
    else:
        direction = "SELL"
        entry = price
        sl = entry + atr
        tp = entry - atr * risk_reward

    # ---------------- LOT SIZE ----------------
    lots = lot_size(balance, risk_pct, entry, sl)

    # ---------------- WINRATE ----------------
    winrate = backtest(df)

    # ---------------- UI CARDS ----------------
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Signal", direction)
    m2.metric("Entry", round(entry,5))
    m3.metric("Stop Loss", round(sl,5))
    m4.metric("Take Profit", round(tp,5))
    m5.metric("Lot Size", lots)
    st.metric("Estimated Win Rate", f"{winrate}%")

    # ---------------- TELEGRAM ----------------
    message = f"""
{symbol} ({mode})
Signal: {direction}
Entry: {round(entry,5)}
SL: {round(sl,5)}
TP: {round(tp,5)}
Lot Size: {lots}
Win Rate: {winrate}%
Session: {current_session()}
"""
    send_telegram(message, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)

    st.success("Signal generated (Telegram sent if configured).")
    st.divider()

    # ---------------- CHART ----------------
    st.line_chart(df[["Close","ema20","ema50"]])

    # ---------------- RECENT DATA ----------------
    with st.expander("Recent Market Data"):
        st.dataframe(df.tail(20))
