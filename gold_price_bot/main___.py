import asyncio
import re
from telethon import TelegramClient, events
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from bot_config import api_id, api_hash, phone_number, bot_token, admin_id, channel_destination
from database_bot import setup_db, update_offsets, get_offsets, update_source_channel, get_source_channel
import nest_asyncio

nest_asyncio.apply()

# ===================== UserBot (Telethon) =======================
user_client = TelegramClient('userbot_session', api_id, api_hash)

application = None

# ===================== Handlers for Telegram Bot =======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != admin_id:
        await update.message.reply_text("You are not authorized.")
        return
    await update.message.reply_text(
        "Welcome Admin!\n"
        "Use /set buy sell to set offsets.\n"
        "Example: /set 3000 -1600\n\n"
        "Use /set_source_channel @channelusername to set the source channel."
    )

async def set_offsets_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != admin_id:
        await update.message.reply_text("Only admin can set offsets.")
        return

    if len(context.args) != 2:
        await update.message.reply_text("Usage: /set buy_offset sell_offset")
        return

    try:
        buy = int(context.args[0])
        sell = int(context.args[1])
    except ValueError:
        await update.message.reply_text("Offsets must be integers.")
        return

    await update_offsets(buy, sell)
    await update.message.reply_text(f"✅ Offsets updated:\nSell: +{buy}\nBuy: {sell:+}")

async def set_source_channel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != admin_id:
        await update.message.reply_text("Only admin can set source channel.")
        return

    if len(context.args) != 1:
        await update.message.reply_text("Usage: /set_source_channel @channelusername")
        return

    source = context.args[0].lower()
    await update_source_channel(source)
    await update.message.reply_text(f"✅ Source channel updated to: {source}")

# ===================== Helper to send message from UserBot handler =======================
async def send_message_to_destination(text):
    global application
    if application is None:
        print("Application not ready yet!")
        return
    try:
        await application.bot.send_message(chat_id=channel_destination, text=text)
    except Exception as e:
        print(f"Error sending message: {e}")

# ===================== UserBot Event Handler =======================
@user_client.on(events.NewMessage)
async def handler(event):
    source_channel = await get_source_channel()
    if not source_channel:
        return

    if event.chat and event.chat.username and f"@{event.chat.username.lower()}" == source_channel:
        text = event.raw_text.strip()
        print("Received from source channel:", text)


        text = re.sub(r"@[\w\d_]+$", "", text).strip()

        buy_offset, sell_offset = await get_offsets()


        def replace_prices(match):
            label = match.group(1) or match.group(3) 
            number = match.group(2) or match.group(4)
            clean_number = int(number.replace(',', ''))

            if 'خرید' in label:
 
                new_price = clean_number + sell_offset
            else:
      
                new_price = clean_number + buy_offset

            return f"{label}{new_price:,}"

        pattern = r"(خرید\s*[:：]\s*)([\d,]+)|(فروش\s*[:：]\s*)([\d,]+)"

        
        new_text = re.sub(pattern, replace_prices, text)

        await send_message_to_destination(new_text)
        print("✅ Edited message sent.")

# ===================== Main Function =======================
async def main():
    global application
    print("Starting...")
    await setup_db()

    await user_client.start(phone=phone_number)
    print("UserBot started.")

    application = ApplicationBuilder().token(bot_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("set", set_offsets_command))
    application.add_handler(CommandHandler("set_source_channel", set_source_channel_command))

    print("Bot started.")

    await asyncio.gather(
        user_client.run_until_disconnected(),
        application.run_polling()
    )

if __name__ == "__main__":
    asyncio.run(main())
