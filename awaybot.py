from telethon import TelegramClient, events
from telethon.tl.types import User
import os, time

api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
session_str = os.environ['SESSION']
session_name = 'away_userbot'

AUTO_REPLY_TEXT = "Привет! Сейчас меня нет на месте. Я отвечу позже 👋"
COOLDOWN_SECONDS = 300

last_replies = {}
enabled = True

client = TelegramClient(session_name, api_id, api_hash)
client.session = session_str  # использовать session-string

@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    sender = await event.get_sender()
    if not isinstance(sender, User) or sender.bot or event.is_group or event.is_channel:
        return
    if not enabled:
        return
    now = time.time()
    if sender.id not in last_replies or now - last_replies[sender.id] >= COOLDOWN_SECONDS:
        await event.reply(AUTO_REPLY_TEXT)
        last_replies[sender.id] = now

@client.on(events.NewMessage(outgoing=True, pattern=r'^\.away (on|off)$'))
async def toggle(event):
    global enabled
    enabled = (event.pattern_match.group(1) == 'on')
    await event.reply(f"АФК автоответ {'включён ✅' if enabled else 'выключен ❌'}.")

print("АФК-бот стартовал")
client.start()
client.run_until_disconnected()
