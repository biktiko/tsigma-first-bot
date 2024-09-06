import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

# Логирование сообщений в файл
def log_message(update):
    with open("log.txt", "a") as log_file:
        log_file.write(f"User {update.effective_user.first_name} ({update.effective_user.id}) said: {update.message.text}\n")

# Обработка команды /start
async def start(update: Update, context):
    log_message(update)
    await update.message.reply_text('Привет! Я усложнённый бот на Heroku. Введите /help для списка команд.')

# Обработка команды /help
async def help_command(update: Update, context):
    log_message(update)
    help_text = """
    Вот что я умею:
    /start - запустить бота
    /help - показать это сообщение
    /about - узнать обо мне
    /random - получить случайное число
    """
    await update.message.reply_text(help_text)

# Обработка команды /about
async def about(update: Update, context):
    log_message(update)
    await update.message.reply_text('Я телеграм-бот, созданный для демонстрации возможностей. Программист: Тигран.')

# Обработка команды /random
async def random_command(update: Update, context):
    log_message(update)
    random_number = random.randint(1, 100)
    await update.message.reply_text(f'Твоё случайное число: {random_number}')

# Обработка кнопок
async def button(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data == "option1":
        await query.edit_message_text(text="Вы выбрали Option 1")
    elif query.data == "option2":
        await query.edit_message_text(text="Вы выбрали Option 2")

# Команда с кнопками
async def choose(update: Update, context):
    log_message(update)
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data="option1"),
            InlineKeyboardButton("Option 2", callback_data="option2"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите опцию:", reply_markup=reply_markup)

if __name__ == '__main__':
    TOKEN = os.getenv('BOT_TOKEN')
    PORT = int(os.environ.get('PORT', '8443'))

    app = ApplicationBuilder().token(TOKEN).build()

    # Добавляем обработчики для команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("random", random_command))
    app.add_handler(CommandHandler("choose", choose))

    # Обработчик для кнопок
    app.add_handler(CallbackQueryHandler(button))

    # Настройка вебхуков
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://tsigma-first-test-bot-f00e73b548b4.herokuapp.com/{TOKEN}"
    )
