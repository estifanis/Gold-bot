import os
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

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
    import asyncio
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check_gold", check_gold))
    app.add_handler(CommandHandler("status", status))
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(auto_loop(app))
    print("Bot is running...")
    app.run_polling()
