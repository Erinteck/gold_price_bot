# 💸 Telegram Price Forwarder Bot

A hybrid Telegram bot using **Telethon** and **python-telegram-bot** that monitors a specific source channel, applies customizable price offsets to Persian "Buy" (`خرید`) and "Sell" (`فروش`) messages, and forwards the modified version to a destination channel.

---

## ✨ Features

- 🔍 Monitors a source channel for new messages (via userbot)
- 🔄 Detects Persian price messages like `خرید: 50000` or `فروش: 80000`
- 🧮 Applies custom offset values to Buy/Sell prices
- 📤 Forwards modified messages to another channel using bot
- 🔐 Admin-only access to configuration commands
- 💾 Stores settings persistently using SQLite (`aiosqlite`)

---

## 📦 Requirements

- Python 3.9 or newer
- Telegram API credentials (from [my.telegram.org](https://my.telegram.org))
- Bot token from [@BotFather](https://t.me/BotFather)
- A Telegram user account (for the userbot session)

### 📥 Install dependencies

```bash
pip install telethon python-telegram-bot aiosqlite nest_asyncio
```

---

## ⚙️ Configuration

Create a file named `bot_config.py` in the project root with the following content:

```python
api_id = 'your api id'
api_hash = 'your api hash'
bot_token = 'your bot token'
admin_id = your_admin_user_id_as_integer
channel_destination = 'your_destination_channel_id_or_username'
phone_number = 'your_registered_phone_number'
```

---

## 🚀 How to Run

```bash
python main___.py
```

---

## 🛠 Available Bot Commands (for Admin)

### `/start`
Shows a welcome/help message.

### `/set <buy_offset> <sell_offset>`
Sets offset values for price adjustment.

Example:
```
/set 3000 -1600
```
This adds **+3000** to "فروش" prices and **-1600** from "خرید" prices.

### `/set_source_channel @channel_username`
Sets the source channel to monitor.

Example:
```
/set_source_channel @yourSourceChannel
```

---

## 🔄 How It Works

1. Userbot (Telethon) listens to the configured source channel.
2. When it detects a message with Persian `خرید:` or `فروش:`, it parses the price.
3. It applies the offset values from settings:
   - `خرید`: uses `sell_offset`
   - `فروش`: uses `buy_offset`
4. It removes any trailing usernames from the text.
5. It sends the final modified message to the destination channel via bot.

---

## 🗃 Database Structure

The SQLite database is stored as `settings.db`.

Table: `settings`

| Column         | Type     | Description                          |
|----------------|----------|--------------------------------------|
| id             | INTEGER  | Always `1` (single row setup)        |
| buy_offset     | INTEGER  | Offset added to فروش (Sell) prices   |
| sell_offset    | INTEGER  | Offset added to خرید (Buy) prices    |
| source_channel | TEXT     | @username of the source channel      |

---

## 🧠 Notes

- Your userbot must stay logged in with a valid Telegram number.
- The destination channel must allow your bot to send messages.
- Don’t run multiple instances of the bot simultaneously.

---

## 🤖 Tech Stack

- [Telethon](https://github.com/LonamiWebs/Telethon) – for userbot session
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) – for admin commands
- [aiosqlite](https://github.com/omnilib/aiosqlite) – for async local database
- [nest_asyncio](https://github.com/erdewit/nest_asyncio) – to run nested event loops

---

## 👨‍💻 Developer

Created and maintained by [**@matinebadi**](https://github.com/matinebadi)  

---
