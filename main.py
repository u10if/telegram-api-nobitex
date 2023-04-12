import requests
import schedule
import time
from telegram import Bot

# Define the API endpoint and chat ID
API_URL = "https://api.nobitex.ir/v2/trades/USDTIRT"
CHAT_ID = "-1001833068446"

# Define the Telegram bot token
BOT_TOKEN = "6194261008:AAHROXD_1CCIvQdzlcx5AUTvDNx3wlD3618"
bot = Bot(token=BOT_TOKEN)

# Define the function that fetches the API data and sends the message
def send_price():
    response = requests.get(API_URL)
    data = response.json()
    latest_price = float(data['trades'][0]['price']) / 10

    if 'prev_latest_price' not in globals():
        global prev_latest_price
        prev_latest_price = latest_price
        text = f'{latest_price}'
    else:
        if latest_price > prev_latest_price:
            text = f'{latest_price} 🔼🟢'
        elif latest_price < prev_latest_price:
            text = f'{latest_price} 🔽🔴'
        else:
            text = f'{latest_price}'

        prev_latest_price = latest_price

    bot.send_message(chat_id=CHAT_ID, text=text)
    print(text)

# Define the interval at which to execute the send_price function
INTERVAL = 60  # seconds

# Schedule the send_price function to run at the specified interval
schedule.every(INTERVAL).seconds.do(send_price)

# Run the scheduled tasks indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)
