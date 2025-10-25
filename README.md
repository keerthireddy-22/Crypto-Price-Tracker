# Crypto-Price-Tracker
Tracks live cryptocurrency prices with alerts

The Crypto Price Tracker project is a real-time web application designed to monitor live cryptocurrency prices and send alerts when specific thresholds are reached. It integrates Streamlit for creating an interactive web interface, CoinGecko API for fetching live market data, Pandas for data management, Plotly for visualizing trends, and smtplib for sending email notifications.

The program begins by allowing users to select multiple cryptocurrencies, such as Bitcoin or Ethereum, and set their own price alert thresholds. It fetches the latest prices using the CoinGecko API and displays them in a neatly formatted table within the Streamlit dashboard. The app updates automatically after a user-defined interval, ensuring that the displayed information remains current.

For visualization, the tracker uses dynamic line charts built with Plotly to show real-time price movements of the selected cryptocurrencies. These charts update continuously, helping users quickly understand market trends and fluctuations. Additionally, when a cryptocurrency crosses the user’s specified price limit—either rising above or dropping below it—the system automatically triggers an email alert using SMTP, notifying the user instantly.

Overall, this project demonstrates the practical use of APIs, data visualization, and automation in Python. It serves as a great example of integrating multiple technologies to build a real-time, user-friendly financial monitoring tool that can be extended to include more advanced analytics or notifications in the future.
