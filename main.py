import os
import time
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

users = {}
participants = []

# Nạp điểm ảo
async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.username
    if not user:
        await update.message.reply_text("Bạn cần đặt username trong Telegram để sử dụng bot.")
        return
    users[user] = users.get(user, 0) + 10
    await update.message.reply_text(f"✅ @{user} đã nạp 10 coin ảo. Số dư: {users[user]}")

# Rút điểm ảo
async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.username
    if users.get(user, 0) >= 10:
        users[user] -= 10
        await update.message.reply_text(f"💸 @{user} đã rút 10 coin. Còn lại: {users[user]}")
    else:
        await update.message.reply_text("❌ Không đủ coin để rút.")

# Tham gia xổ số
async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.username
    if not user:
        await update.message.reply_text("Bạn cần đặt username trong Telegram.")
        return
    if user in participants:
        await update.message.reply_text("Bạn đã tham gia rồi!")
    else:
        participants.append(user)
        await update.message.reply_text(f"🎫 @{user} đã tham gia xổ số.")

# Quay xổ số
async def draw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not participants:
        await update.message.reply_text("Không có ai tham gia cả.")
        return
    winner = random.choice(participants)
    await update.message.reply_text(f"🏆 Người chiến thắng là: @{winner}")
    participants.clear()

# Kiểm tra số dư
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.username
    bal = users.get(user, 0)
    await update.message.reply_text(f"💰 Số dư của @{user}: {bal} coin")

# Khởi tạo bot
app = ApplicationBuilder().token(os.environ["TOKEN"]).build()

# Thêm lệnh
app.add_handler(CommandHandler("deposit", deposit))
app.add_handler(CommandHandler("withdraw", withdraw))
app.add_handler(CommandHandler("join", join))
app.add_handler(CommandHandler("draw", draw))
app.add_handler(CommandHandler("balance", balance))

# Chạy bot có tự động reconnect và timeout
print("Bot đang chạy...")
while True:
    try:
        app.run_polling(timeout=60)
    except Exception as e:
        print(f"Lỗi: {e}. Đang thử lại sau 5 giây...")
        time.sleep(5)

