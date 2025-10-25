import streamlit as st
import requests
import pandas as pd
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import plotly.express as px

# ============ EMAIL ALERT FUNCTION ============
def send_email_alert(coin, price, threshold, email):
    sender = "youremail@gmail.com"  # Replace with your email
    password = "yourpassword"       # App password (not regular password)
    
    subject = f"Crypto Alert: {coin.capitalize()} crossed your threshold!"
    body = f"The current price of {coin.capitalize()} is ${price}, which {'rose above' if price > threshold else 'fell below'} your set threshold (${threshold})."

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
        st.success(f"📧 Email sent to {email}")
    except Exception as e:
        st.error(f"Failed to send email: {e}")

# ============ FETCH CRYPTO PRICES ============
def get_crypto_prices(coin_ids):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(coin_ids)}&vs_currencies=usd"
    response = requests.get(url)
    return response.json()

# ============ STREAMLIT UI ============
st.title("💰 Crypto Price Tracker")
st.markdown("Track live cryptocurrency prices and get alerts when thresholds are hit!")

coins = st.multiselect("Select Cryptocurrencies", 
                       ["bitcoin", "ethereum", "dogecoin", "solana", "cardano"], 
                       default=["bitcoin", "ethereum"])

email = st.text_input("Enter your email for alerts (optional):")
thresholds = {}
for coin in coins:
    thresholds[coin] = st.number_input(f"Set alert threshold for {coin} (USD):", min_value=0.0, value=0.0, step=10.0)

refresh_time = st.slider("Auto-refresh every (seconds):", 10, 120, 30)

price_data = []
chart_data = pd.DataFrame()

placeholder = st.empty()

while True:
    data = get_crypto_prices(coins)
    current_time = pd.Timestamp.now()
    prices = {coin: float(data[coin]['usd']) for coin in coins}  # ensure numeric

    # Add to chart data
    new_row = {"time": current_time}
    new_row.update(prices)
    chart_data = pd.concat([chart_data, pd.DataFrame([new_row])], ignore_index=True)

    # Convert all crypto columns to numeric
    for coin in coins:
        chart_data[coin] = pd.to_numeric(chart_data[coin], errors='coerce')

    # Display prices
    df = pd.DataFrame(list(prices.items()), columns=["Coin", "Price (USD)"])
    
    with placeholder.container():
        st.subheader("📊 Current Prices")
        st.table(df)
        
        if len(chart_data) > 1:  # Plot only if we have data
            st.subheader("📈 Price Trends")
            fig = px.line(chart_data, x="time", y=coins, title="Live Price Trends")
            st.plotly_chart(fig, use_container_width=True)
    
    # Check alerts
    if email:
        for coin, price in prices.items():
            threshold = thresholds[coin]
            if threshold > 0 and ((price >= threshold) or (price <= threshold)):
                send_email_alert(coin, price, threshold, email)
    
    time.sleep(refresh_time)
