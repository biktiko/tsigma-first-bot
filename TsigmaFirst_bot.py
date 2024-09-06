import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

async def start(update: Update, context):
    await update.message.reply_text('Привет! Я работаю на Heroku.')

if __name__ == '__main__':
    TOKEN = os.getenv('BOT_TOKEN')  # Используем токен из переменных среды
    PORT = int(os.environ.get('PORT', '8443'))  # Heroku использует переменную PORT

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # Настройка вебхуков
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://<твоё-приложение>.herokuapp.com/{TOKEN}"
    )
