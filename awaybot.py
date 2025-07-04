import os, time
from telethon import TelegramClient, events
from telethon.tl.types import User

api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
session_string = os.environ['SESSION']

# Используем сессию из строки для автологина
client = TelegramClient(StringSession(session_string), api_id, api_hash)

AUTO_REPLY_TEXT = "Ожидай, отвечу позже ⏳"
COOLDOWN_SECONDS = 300

last_replies = {}
enabled = True

@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    sender = await event.get_sender()
    if not isinstance(sender, User) or sender.bot or event.is_group or event.is_channel:
        return
    if not enabled:
        return
    now = time.time()
    uid = sender.id
    if uid not in last_replies or now - last_replies[uid] >= COOLDOWN_SECONDS:
        await event.reply(AUTO_REPLY_TEXT)
        last_replies[uid] = now

@client.on(events.NewMessage(outgoing=True, pattern=r'^\.away (on|off)$'))
async def toggle(event):
    global enabled
    enabled = event.pattern_match.group(1) == 'on'
    await event.reply(f"АФК автоответ {'включён ✅' if enabled else 'выключен ❌'}.")

print("АФК-бот запущен и работает.")
client.start()
client.run_until_disconnected()
