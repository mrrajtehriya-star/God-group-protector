import telebot
import os
from keep_alive import keep_alive

# Environment variable se token fetch karega
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# --- START COMMAND ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """👑 *WELCOME TO GROUP PROTECTOR* 👑

✨ Ye ek powerful Group Protector + Helper Bot hai. Aapke group ko ekdam chill zone bana dega! 😎
🛡️ Spam, Raid, aur Abuse karne walon ko seedha block-list ka rasta dikhayega.

⚡ *Features:*
• Auto Protection System
• TagAll System
• Admin Controls
• Filter & Anti-Link

👤 *Owner:* The Ultimate Boss 😎

🚀 Bot ko group me add karo aur admin bana do...
phir dekho iska asli power! 💀🔥"""
    
    # Aapki image ki public link yahan aayegi
    photo_url = "https://images.unsplash.com/photo-1529156069898-49953e39b3ac"
    bot.send_photo(message.chat.id, photo=photo_url, caption=welcome_text, parse_mode="Markdown")

# --- HELP COMMAND ---
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """🔥 *GROUP PROTECTOR - COMMAND LIST* 🔥

👥 *USER:* `/start` `/help` `/donate` `/geturl` `/pinned` `/me` `/staff`
👮 *ADMIN:* `/ban` `/unban` `/kick` `/mute` `/unmute` `/info` `/infopvt` `/warn` `/unwarn` `/warns` `/delwarn` `/reload` `/intervention`
👑 *OWNER:* `/addowner` `/removeowner` `/addsudo` `/removesudo` `/broadcast` `/restart` `/shutdown` `/banall` `/leaveall` `/stats` `/logs`
🔐 *SECURITY:* `/antiflood` `/setflood` `/antibot` `/antilink` `/antiarabic` `/antitagall` `/captcha` `/welcome` `/setwelcome` `/goodbye` `/setgoodbye`
🚫 *MODERATION:* `/filter` `/stop` `/filters` `/lock` `/unlock`
🤖 *AUTO REPLY:* `/setreply` `/delreply` `/replies` `/autoreply`
🎯 *EXTRAS:* `/notes` `/get` `/clear` `/tagall` `/admins` `/poll`
🏘️ *GROUP TOOLS:* `/promote` `/demote` `/pin` `/unpin` `/unpinall` `/del` `/purge` `/report` `/id` `/invite` `/kickme` `/slowmode` `/tmute` `/tban` `/groupinfo` `/membercount` `/listadmins` `/setgrouptitle` `/setdescription`"""
    
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

# --- BOT STARTUP ---
keep_alive()
print("Group Protector Bot is running...")
bot.infinity_polling()
