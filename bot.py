from telegram import Bot
from websocket import create_connection
import talib
import numpy as np
import json
import time

TELEGRAM_TOKEN = "8380179787:AAF9cjpvovkQpgxsKP9W6gp71oZTzoBp2Vo"
CHAT_ID = 7555062484

bot = Bot(token=TELEGRAM_TOKEN)

def send_signal(signal_type, price, timestamp):
    message = f"📊 إشارة جديدة:\n🔹 نوع الإشارة: {signal_type}\n🔹 السعر: {price}\n🔹 الوقت: {timestamp}"
    bot.send_message(chat_id=CHAT_ID, text=message)

def analyze_market(prices):
    rsi = talib.RSI(np.array(prices), timeperiod=14)[-1]
    macd, signal, hist = talib.MACD(np.array(prices), fastperiod=12, slowperiod=26, signalperiod=9)
    if rsi < 30 and macd[-1] > signal[-1]:
        return "شراء"
    elif rsi > 70 and macd[-1] < signal[-1]:
        return "بيع"
    return None

def main():
    ws = create_connection("wss://api.pocketoption.com/marketdata")  # مثال
    prices = []
    while True:
        result = json.loads(ws.recv())
        prices.append(result["price"])
        if len(prices) > 100:
            prices.pop(0)
        signal = analyze_market(prices)
        if signal:
            send_signal(signal, prices[-1], time.strftime("%H:%M:%S"))
        time.sleep(1)

if __name__ == "__main__":
    main()
