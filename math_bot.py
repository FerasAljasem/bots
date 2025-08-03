from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.getenv("TOKEN_TG")
if not TOKEN:
    raise ValueError("Error: TOKEN environment variable is not set.")



# الأسئلة الكاملة
questions = {
    "1": ("🍎", "1", ["1", "2", "3"]),
    "2": ("🍎🍎", "2", ["1", "2", "3"]),
    "3": ("🍎🍎🍎", "3", ["2", "3", "4"]),
    "4": ("🍎🍎🍎🍎", "4", ["3", "4", "5"]),
    "5": ("🍎🍎🍎🍎🍎", "5", ["4", "5", "6"]),
}

# عرض القائمة الأولى
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(f"🔢 العدد {i}", callback_data=f"start_{i}")]
        for i in range(1, 6)
    ]
    await update.message.reply_text(
        "👋 أهلًا بك!\nاختر العدد الذي تريد البدء منه:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# عند الضغط على زر عدد أو إجابة
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # بدء سؤال محدد
    if data.startswith("start_"):
        number = data.split("_")[1]
        await send_question(query, number)

    # إجابة الطالب
    elif data.startswith("a_"):
        correct, chosen, current = data.split("_")[1:]
        if chosen == correct:
            await query.message.reply_text("✅ إجابة صحيحة! أحسنت!")
            next_q = str(int(current) + 1)
            if next_q in questions:
                await send_question(query, next_q)
            else:
                await query.message.reply_text("🎉 انتهت التمارين! ممتاز 👏")
        else:
            await query.message.reply_text("❌ خطأ، حاول مرة أخرى.")
            await send_question(query, current)  # أعد نفس السؤال

# توليد سؤال
async def send_question(query, number):
    content, correct, options = questions[number]
    buttons = [
        [InlineKeyboardButton(opt, callback_data=f"a_{correct}_{opt}_{number}")]
        for opt in options
    ]
    await query.message.reply_text(
        f"{content}\nكم عدد التفاحات؟",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# التشغيل
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handler))
    app.run_polling()

if __name__ == "__main__":
    main()





