import os
import asyncio
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler

# Render Port ስህተት እንዳያሳይ ቀላል Web Server
web_app = Flask('')

@web_app.route('/')
def home():
    return "Bot is live!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

TELEGRAM_BOT_TOKEN = "8969181755:AAFJh5HVlmcM5sqOgPPo8b5lDecWRKz8Rv8" 
async def start(update, context):
    await update.message.reply_text("Bot is active!")

async def check_gold(update, context):
    await update.message.reply_text("Checking gold status...")

async def status(update, context):
    await update.message.reply_text("System running smoothly.")

async def auto_loop(app):
    while True:
        try:
            print("Running background check...")
            await asyncio.sleep(15)
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(15)

if __name__ == '__main__':
    # Flask ሰርቨር በጀርባ እንዲሰራ ማድረግ
    t = Thread(target=run_flask)
    t.start()

    # Telegram Bot ማስነሳት
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check_gold", check_gold))
    app.add_handler(CommandHandler("status", status))
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(auto_loop(app))
    print("Bot is running...")
    app.run_polling()
