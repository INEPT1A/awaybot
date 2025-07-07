import os, time
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import User

# Получаем данные из окружения
api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
session_string = os.environ['SESSION']

client = TelegramClient(StringSession(session_string), api_id, api_hash)

# Основные настройки
AUTO_REPLY_TEXT = "Ожидай, отвечу позже ⏳"
COOLDOWN_SECONDS = 300
enabled = True
last_replies = {}
ignored_chats = set()

@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    sender = await event.get_sender()

    if (
        not isinstance(sender, User) or
        sender.bot or
        event.is_group or
        event.is_channel or
        not enabled or
        event.chat_id in ignored_chats
    ):
        return

    now = time.time()
    uid = sender.id
    if uid not in last_replies or now - last_replies[uid] >= COOLDOWN_SECONDS:
        await event.reply(AUTO_REPLY_TEXT)
        last_replies[uid] = now

@client.on(events.NewMessage(outgoing=True, pattern=r'^\.away (on|off)$'))
async def toggle_afk(event):
    global enabled
    enabled = event.pattern_match.group(1) == 'on'
    await event.reply(f"АФК автоответ {'включён ✅' if enabled else 'выключен ❌'}.")

@client.on(events.NewMessage(outgoing=True, pattern=r'^\.away (\-?\d+) (on|off)$'))
async def toggle_chat_ignore(event):
    chat_id = int(event.pattern_match.group(1))
    action = event.pattern_match.group(2)

    if action == 'off':
        ignored_chats.add(chat_id)
        await event.reply(f"АФК отключён в чате `{chat_id}` ❌")
    else:
        ignored_chats.discard(chat_id)
        await event.reply(f"АФК включён в чате `{chat_id}` ✅")

print("АФК-бот запущен и работает.")
client.start()
client.run_until_disconnected()
