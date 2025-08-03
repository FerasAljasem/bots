from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("Error: TOKEN environment variable is not set.")

questions = {
    "1": ("🍎", "1", ["1", "2", "3"]),
    "2": ("🍎🍎", "2", ["1", "2", "3"]),
    "3": ("🍎🍎🍎", "3", ["2", "3", "4"]),
    "4": ("🍎🍎🍎🍎", "4", ["3", "4", "5"]),
    "5": ("🍎🍎🍎🍎🍎", "5", ["4", "5", "6"]),
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(f"🔢 العدد {i}", callback_data=f"start_{i}")]
        for i in range(1, 6)
    ]
    await update.message.reply_text(
        "👋 أهلًا بك!\nاختر العدد الذي تريد البدء منه:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("start_"):
        number = data.split("_")[1]
        await send_question(query, number)

    elif data.startswith("a_"):
        correct, chosen, current = data.split("_")[1:]
        if chosen == correct:
            await query.edit_message_text("✅ إجابة صحيحة! أحسنت!")
            next_q = str(int(current) + 1)
            if next_q in questions:
                await send_question(query, next_q)
            else:
                await query.message.reply_text("🎉 انتهت التمارين! ممتاز 👏")
        else:
            await query.answer("❌ خطأ، حاول مرة أخرى.", show_alert=True)
            await send_question(query, current)  # إعادة نفس السؤال

async def send_question(query, number):
    content, correct, options = questions[number]
    buttons = [
        [InlineKeyboardButton(opt, callback_data=f"a_{correct}_{opt}_{number}")]
        for opt in options
    ]
    await query.edit_message_text(
        f"{content}\nكم عدد التفاحات؟",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handler))
    app.run_polling()

if __name__ == "__main__":
    main()
