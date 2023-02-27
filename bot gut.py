import requests
import json
import time
from telegram import Bot

# Define the API endpoint and chat ID
API_URL = "https://api.nobitex.ir/market/stats"
CHAT_ID = "YOUR chat id"

# Define the parameters for the API request
PARAMS = {
    "srcCurrency": "usdt",
    "dstCurrency": "rls"
}

# Define the Telegram bot token
BOT_TOKEN = "bot token"
bot = Bot(token=BOT_TOKEN)

# Define the interval for sending messages (in seconds)
INTERVAL = 60

# Define the function that fetches the API data and sends the message
def send_price():
    # Send the POST request with the specified parameters
    response = requests.post(API_URL, headers={"Content-Type": "application/json"}, json=PARAMS)

    # Extract the bestSell value from the JSON data
    data = response.json()
    best_sell = float(data['stats']['usdt-rls']['latest']) / 10

    # Check if prev_best_sell has been defined as a global variable
    if 'prev_best_sell' not in globals():
        global prev_best_sell
        prev_best_sell = best_sell
        text = f' {best_sell}'
    else:
        # Compare the current best_sell value with the previous value
        if best_sell > prev_best_sell:
            text = f' {best_sell} 🔼🟢'
        elif best_sell < prev_best_sell:
            text = f' {best_sell} 🔽🔴'
        else:
            text = f' {best_sell}'

        # Update the previous best_sell value
        prev_best_sell = best_sell

    # Send the message to the Telegram chat
    bot.send_message(chat_id=CHAT_ID, text=text)

    print(text)

# Loop indefinitely and send messages every INTERVAL seconds
while True:
    send_price()
    time.sleep(INTERVAL)
