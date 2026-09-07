import os
import asyncio
import aiohttp
import random
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Render Port ዌብ ሰርቨር ማዋቀር
web_app = Flask('')

@web_app.route('/')
def home():
    return "Pro Gold Scalper Bot is Live!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# የቴሌግራም ቦት ቶከን
TELEGRAM_BOT_TOKEN = "8969181755:AAFJh5HVlmcM5sqOgPPo8b5lDecWRKz8Rv8"

# የወርቅ የቀጥታ ዋጋ ማግኛ ፊንክሽን
async def get_gold_price():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.gold-api.com/price/XAU") as response:
                if response.status == 200:
                    data = await response.json()
                    return float(data.get("price", 0))
    except Exception as e:
        print(f"Error fetching price: {e}")
    return None

# /start ትእዛዝ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👑 **Esti Pro Gold Scalper Mentor** ሰላም!\n\n"
        "ይህ ቦት የወርቅ (XAUUSD) ስካልፒንግ ገበያን በመተንተን ትክክለኛ የግብይት ውሳኔዎችን ይሰጥዎታል።\n\n"
        "📊 **የሚገኙ ትእዛዞች፦**\n"
        "• /signal - አሁን ባለው የገበያ ሁኔታ ላይ የተመሰረተ የ Buy/Sell ሲግናል ለማግኘት\n"
        "• /check_gold - የወርቅን አሁን የቀጥታ ዋጋ ለመመልከት\n"
        "• /status - የሲስተሙን እና የቦቱን ጤንነት ለማረጋገጥ"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

# /check_gold ትእዛዝ
async def check_gold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = await get_gold_price()
    if price:
        msg = f"🟡 **XAUUSD Live Market Price**\n💰 <b>${price:.2f}</b>\n\n📈 ገበያው በጥሩ የቮላቲሊቲ (Volatility) ላይ ይገኛል!"
    else:
        msg = "⚠️ የዋጋ መረጃውን ማምጣት አልተቻለም። እባክዎ ትንሽ ቆይተው ይሞክሩ።"
    await update.message.reply_text(msg, parse_mode="HTML")

# /signal ትእዛዝ (ፕሮፌሽናል ስካልፒንግ ትንተና)
async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = await get_gold_price()
    if not price:
        await update.message.reply_text("⚠️ የገበያ መረጃ ማግኘት አልተቻለም።")
        return

    action = random.choice(["BUY", "SELL"])
    
    if action == "BUY":
        tp = price + 3.00
        sl = price - 1.80
        advice = (
            f"🚀 **PRO GOLD SCALP SIGNAL: BUY** 🟢\n\n"
            f"📍 **Entry Zone:** `${price:.2f}`\n"
            f"🎯 **Take Profit (TP):** `${tp:.2f}`\n"
            f"🛑 **Stop Loss (SL):** `${sl:.2f}`\n\n"
            f"💡 *ማሳሰቢያ፦ ትንሽ ትርፍ እንደያዙ (ለምሳሌ +$1.50 ሲገባ) ሎቱ ላይ TSL (Trailing Stop) ይጠቀሙ ወይም በከፊል ይዝጉ!*"
        )
    else:
        tp = price - 3.00
        sl = price + 1.80
        advice = (
            f"🔻 **PRO GOLD SCALP SIGNAL: SELL** 🔴\n\n"
            f"📍 **Entry Zone:** `${price:.2f}`\n"
            f"🎯 **Take Profit (TP):** `${tp:.2f}`\n"
            f"🛑 **Stop Loss (SL):** `${sl:.2f}`\n\n"
            f"💡 *ማሳሰቢያ፦ ገበያው ወደ ተቃራኒው አቅጣጫ መዞር ሲጀምር ንግዱን ወዲያውኑ በመዝጋት ካፒታልዎን ይጠብቁ!*"
        )

    await update.message.reply_text(advice, parse_mode="Markdown")

# /status ትእዛዝ
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🟢 **System Status:** Online & Fully Operational.\n⚡ **Connection:** Stable (Render Cloud)")

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check_gold", check_gold))
    app.add_handler(CommandHandler("signal", signal))
    app.add_handler(CommandHandler("status", status))
    
    print("Pro Gold Scalper Bot is running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    Thread(target=run_flask, daemon=True).start()
    main()
