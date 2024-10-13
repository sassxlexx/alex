from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait

from uu import *


__MODULE__ = "Spam"
__HELP__ = """
<b>Menu Spam!</b>

<b>Spamming broadcast!</b>
 <code>{0}spamg</code>

<b>Spamming message!</b>
 <code>{0}spam</code>

<b>Delay spamming message!</b>(ultra)
 <code>{0}dspam</code>

<b>Set delay spamming!</b>(ultra)
 <code>{0}setdelay</code>

<b>Example!</b>
 <code>fastspam = to faster spam</code>
 <code>slowspam = to slowed spam</code>
"""


total_spam_gcast = {}
SPAM_COUNT = [0]


def increment_spam_count():
    SPAM_COUNT[0] += 1
    return spam_allowed()


def spam_allowed():
    return SPAM_COUNT[0] < 50


async def SpamMsg(client, message, send):
    delay = await DB.get_vars(client.me.id, "spam_delay") or 1
    await asyncio.sleep(int(delay))
    if message.reply_to_message:
        await send.copy(message.chat.id)
    else:
        await client.send_message(message.chat.id, send)


async def SpamGcast(client, message, send):
    blacklist = await DB.get_list_vars(client.me.id, "blacklist")
    total_spam_gcast[client.me.id] = 0

    async def send_message(target_chat):
        await asyncio.sleep(0.8)
        if message.reply_to_message:
            await send.copy(target_chat)
        else:
            await client.send_message(target_chat, send)

    async def handle_flood_wait(exception, target_chat):
        await asyncio.sleep(exception.value)
        await send_message(target_chat)

    async for dialog in client.get_dialogs():
        if dialog.chat.type in {ChatType.GROUP, ChatType.SUPERGROUP} and dialog.chat.id not in blacklist:
            try:
                await send_message(dialog.chat.id)
                total_spam_gcast[client.me.id] += 1
            except FloodWait as e:
                await handle_flood_wait(e, dialog.chat.id)
                total_spam_gcast[client.me.id] += 1
            except Exception:
                pass



@PY.UBOT("dspam")
@PY.ULTRA
async def _(client, message):
    _msg = "<b>Processing...</b>"

    r = await message.reply(_msg)
    count, msg = type_and_msg(message)

    try:
        count = int(count)
    except Exception:
        return await r.edit(f"<b><code>{message.text.split()[0]}</code> amount - text/reply!</b>")

    if not msg:
        return await r.edit(
            f"<b><code>{message.text.split()[0]}</code> amount - text/reply!</b>"
        )
    
    for _ in range(count):
        await SpamMsg(client, message, msg)
    
    await r.edit("<b>Delay spam succes!</b>")


@PY.UBOT("setdelay")
@PY.ULTRA
async def _(client, message):
    _msg = "<b>Processing...</b>"

    r = await message.reply(_msg)
    count, msg = type_and_msg(message)

    try:
        count = int(count)
    except Exception:
        return await r.edit(f"<b><code>{message.text.split()[0]}</code> count!</b>")

    if not count:
        return await r.edit(f"<b><code>{message.text.split()[0]}</code> count!</b>")

    await DB.set_vars(client.me.id, "spam_delay", count)
    return await r.edit("<b>Spam delay has been set!</b>")


@PY.UBOT("spamg")
async def _(client, message):
    r = await message.reply(f"<b>Processing...</b>")
    count, msg = type_and_msg(message)

    if not msg:
        return await r.edit(f"<b><code>{message.text.split()[0]}</code> count - text/reply</b>")

    try:
        count = int(count)
    except Exception as error:
        return await r.edit(error)

    async def run_spam():
        spam_gcast = [SpamGcast(client, message, msg) for _ in range(int(count))]
        await asyncio.gather(*spam_gcast)

    await run_spam()
    await r.edit(f"<b>Success spam gcast!\nDone: <code>{int(total_spam_gcast[client.me.id] / count)}</code> group\nRound: <code>{count}</code></b>")
    del total_spam_gcast[client.me.id]


@PY.UBOT("spam|statspam|slowspam|fastspam")
async def _(client, message):
    try:
        amount = int(message.command[1])
        text = " ".join(message.command[2:])
    except (IndexError, ValueError):
        return await message.reply("<b>Invalid command format!</b>")
    
    cooldown = {"spam": 0.15, "statspam": 0.1, "slowspam": 0.9, "fastspam": 0}

    if not text:
        return await message.reply("<b>Message empty!</b>")

    await message.delete()
    
    for msg in range(amount):
        if message.reply_to_message:
            sent = await message.reply_to_message.reply(text)
        else:
            sent = await client.send_message(message.chat.id, text)

        if message.command[0] == "statspam":
            await asyncio.sleep(0.1)
            await sent.delete()

        await asyncio.sleep(cooldown[message.command[0]])
