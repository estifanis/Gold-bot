import time
import requests
import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_TOKEN = "8969181755:AAFJh5HV1mcM5sq0gPPo8b51DecWRKz8Rv8"
MY_CHAT_ID = "8355743589"

SYMBOL = "XAUUSD"

def get_gold_price():
    try:
        url = "https://api.gold-api.com/price/XAU"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return float(response.json()['price'])
    except Exception as e:
        print(f"Error: {e}")
    return None

prices_history = []

def analyze_scalp():
    global prices_history
    price = get_gold_price()
    
    if not price:
        return "WAIT", 0.0

    prices_history.append(price)
    if len(prices_history) > 10:
        prices_history.pop(0)

    if len(prices_history) < 3:
        return "WAIT", price

    avg_price = sum(prices_history) / len(prices_history)
    
    if price > avg_price + 0.30:
        return "BUY", price
    elif price < avg_price - 0.30:
        return "SELL", price
        
    return "WAIT", price

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != str(MY_CHAT_ID):
        return
    keyboard = [["/check_gold", "/status"]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("🏆 **Gold Scalper Bot ስራ ጀምሯል!**\n\nከ Stop Loss (SL) ውጪ ለ Scalping የተዘጋጀ ነው።", reply_markup=markup, parse_mode="Markdown")

async def check_gold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != str(MY_CHAT_ID):
        return
    signal, price = analyze_scalp()
    await update.message.reply_text(f"📊 **XAUUSD (Gold)**\n\n💰 ዋጋ: **${price:.2f}**\n⚡ Signal: **{signal}**", parse_mode="Markdown")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != str(MY_CHAT_ID):
        return
    await update.message.reply_text("✅ ቦቱ በህይወት አለ፤ 24 ሰዓት ይከታተላል!")

async def auto_loop(app):
    last_signal = "WAIT"
    while True:
        try:
            signal, price = analyze_scalp()
            if signal in ["BUY", "SELL"] and signal != last_signal:
                last_signal = signal
                msg = (
                    f"🔥 **[GOLD SCALP SIGNAL]**\n\n"
                    f"📈 **Action:** {signal}\n"
                    f"💵 **Price:** ${price:.2f}\n"
                    f"🎯 **Target Profit (TP):** 15 Pips\n"
                    f"🚫 **Stop Loss (SL):** No SL\n\n"
                    f"👉 አሁን በ MT5 አፕህ ገብተህ {signal} ክፈት!"
                )
                await app.bot.send_message(chat_id=MY_CHAT_ID, text=msg, parse_mode="Markdown")
            elif signal == "WAIT":
                last_signal = "WAIT"
        except Exception as e:
            print(f"Error: {e}")
        await asyncio.sleep(15)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check_gold", check_gold))
    app.add_handler(CommandHandler("status", status))
    
    loop = asyncio.get_event_loop()
    loop.create_task(auto_loop(app))
    
    print("Bot is running...")
    app.run_polling()
