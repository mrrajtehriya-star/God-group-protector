import os
import telebot
import sqlite3
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# 📦 DATABASE
conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS warns (user_id INTEGER, count INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS replies (word TEXT, reply TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS filters (word TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS notes (name TEXT, text TEXT)")
conn.commit()

# ✅ START
@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("➕ Add Me", url="https://t.me/YOUR_BOT_USERNAME?startgroup=true"))

    bot.send_photo(
        message.chat.id,
        "https://i.imgur.com/yourimage.jpg",
        caption="🤖 Welcome!\n/help likho commands ke liye 🔥",
        reply_markup=markup
    )

# ✅ HELP
@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.send_message(message.chat.id, "📜 Commands list:\n/start\n/help\n/ban\n/warn\n/setreply\n/notes ...")

# =========================
# ⚠️ WARN SYSTEM
# =========================
@bot.message_handler(commands=['warn'])
def warn_user(message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id

        cursor.execute("SELECT count FROM warns WHERE user_id=?", (user_id,))
        data = cursor.fetchone()

        if data:
            count = data[0] + 1
            cursor.execute("UPDATE warns SET count=? WHERE user_id=?", (count, user_id))
        else:
            count = 1
            cursor.execute("INSERT INTO warns VALUES (?,?)", (user_id, count))

        conn.commit()
        bot.send_message(message.chat.id, f"⚠️ User warned! Total warns: {count}")

# =========================
# 🔨 BAN / KICK / MUTE
# =========================
@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message:
        bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)

@bot.message_handler(commands=['kick'])
def kick_user(message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user.id
        bot.ban_chat_member(message.chat.id, user)
        bot.unban_chat_member(message.chat.id, user)

@bot.message_handler(commands=['mute'])
def mute_user(message):
    if message.reply_to_message:
        bot.restrict_chat_member(
            message.chat.id,
            message.reply_to_message.from_user.id,
            permissions=telebot.types.ChatPermissions(can_send_messages=False)
        )

# =========================
# 🤖 AUTO REPLY
# =========================
@bot.message_handler(commands=['setreply'])
def set_reply(message):
    try:
        _, word, reply = message.text.split(" ", 2)
        cursor.execute("INSERT INTO replies VALUES (?,?)", (word.lower(), reply))
        conn.commit()
        bot.reply_to(message, "✅ Auto reply set")
    except:
        bot.reply_to(message, "Usage: /setreply hi Hello")

@bot.message_handler(func=lambda m: True)
def auto_reply(message):
    text = message.text.lower()

    # 🔁 Replies
    cursor.execute("SELECT * FROM replies")
    for word, reply in cursor.fetchall():
        if word in text:
            bot.reply_to(message, reply)

    # 🚫 Filters
    cursor.execute("SELECT word FROM filters")
    for (word,) in cursor.fetchall():
        if word in text:
            bot.delete_message(message.chat.id, message.message_id)

    # 🔗 Anti-link
    if "http" in text:
        bot.delete_message(message.chat.id, message.message_id)

# =========================
# 🚫 FILTER SYSTEM
# =========================
@bot.message_handler(commands=['filter'])
def add_filter(message):
    word = message.text.split(" ", 1)[1]
    cursor.execute("INSERT INTO filters VALUES (?)", (word,))
    conn.commit()
    bot.reply_to(message, "✅ Word banned")

# =========================
# 📝 NOTES SYSTEM
# =========================
@bot.message_handler(commands=['notes'])
def save_note(message):
    try:
        _, name, text = message.text.split(" ", 2)
        cursor.execute("INSERT INTO notes VALUES (?,?)", (name, text))
        conn.commit()
        bot.reply_to(message, "✅ Note saved")
    except:
        bot.reply_to(message, "Usage: /notes name text")

@bot.message_handler(commands=['get'])
def get_note(message):
    name = message.text.split(" ", 1)[1]
    cursor.execute("SELECT text FROM notes WHERE name=?", (name,))
    data = cursor.fetchone()
    if data:
        bot.send_message(message.chat.id, data[0])

# =========================

print("🚀 Bot Running...")
bot.infinity_polling()
