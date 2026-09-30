import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# BotFather bergan TOKEN ni shu yerga yozing:
BOT_TOKEN = "8744240008:AAFJfENrydrUh13j64RFG0q9gaPiPsFfXnc"

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [KeyboardButton("Taxi chaqirish 🚕")],
        [KeyboardButton("Biz haqimizda ℹ️"), KeyboardButton("Bog'lanish 📞")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        f"Assalomu alaykum, {user.first_name}!\nTaxi xizmatimiz botiga xush kelibsiz.",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "Taxi chaqirish 🚕":
        location_keyboard = [[KeyboardButton("Joylashuvni yuborish 📍", request_location=True)]]
        markup = ReplyKeyboardMarkup(location_keyboard, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text("Iltimos, turgan joyingizni yuboring:", reply_markup=markup)
        
    elif text == "Biz haqimizda ℹ️️":
        await update.message.reply_text("Bizning Taxi xizmati 24/7 rejimida tez va xavfsiz xizmat ko'rsatadi.")
        
    elif text == "Bog'lanish 📞":
        await update.message.reply_text("Operator bilan bog'lanish: +998 90 123 45 67")

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.location
    await update.message.reply_text(
        f"Rahmat! Joylashuvingiz qabul qilindi:\n"
        f"Kenglik: {location.latitude}\n"
        f"Uzunlik: {location.longitude}\n\n"
        f"Haydovchi tez orada siz bilan bog'lanadi!"
    )

if __name__ == "__main__":
        app = ApplicationBuilder().token(BOT_TOKEN).build()


    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))

    print("Bot ishga tushdi...")
    app.run_polling(drop_pending_updates=True)
