import asyncio
from datetime import datetime
from time import time

from pyrogram.raw.functions import Ping

from uu import *



async def load_ping_messages(client):
    ping_message = {}

    ping_message["pong"] = await DB.get_vars(client.me.id, "PONG") or "ᴘᴏɴɢ:"
    ping_message["owner"] = await DB.get_vars(client.me.id, "OWNER") or "ᴏᴡɴᴇʀ:"
    ping_message["ubot"] = await DB.get_vars(client.me.id, "UBOT") or "ʙʏ : ᴋᴀɴᴀᴇʀᴜ"

    return ping_message


@PY.UBOT("ping|p")
async def _(client, message):
    user_id = message.from_user.id
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    end = datetime.now()
    ping_msg = await load_ping_messages(client)
    delta_ping = (end - start).microseconds / 1000
    delta_ping_formatted = round(delta_ping)
    pong = await EMO.PING(client)
    tion = await EMO.MENTION(client)
    yubot = await EMO.UBOT(client)
    if client.me.is_premium:
       _ping = f"""
<blockquote>{pong}-ˋˏ⛥┈ <b>{ping_msg["pong"]}</b> <code>{str(delta_ping_formatted).replace('.', ',')} ᴍs</code>
{tion}-ˋˏ⛥┈ <b>{ping_msg["owner"]}</b> <code>{client.me.mention}</code>
{yubot}-ˋˏ⛥┈ <b>{ping_msg["ubot"]}</b></blockquote>
"""
    else:
       _ping = f"""
<blockquote><b><pre{ping_msg["pong"]}</b></pre> <code>{str(delta_ping_formatted).replace('.', ',')} ᴍs</code>
"""
    await message.reply(_ping)

@TU.on_message(filters.user(Config.OWNER_ID) & filters.command("cping|cp", ""))
async def _(client, message):
    user_id = message.from_user.id
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    end = datetime.now()
    ping_msg = await load_ping_messages(client)
    delta_ping = (end - start).microseconds / 1000
    delta_ping_formatted = round(delta_ping)
    pong = await EMO.PING(client)
    tion = await EMO.MENTION(client)
    yubot = await EMO.UBOT(client)
    if client.me.is_premium:
       _ping = f"""
<blockquote>{pong}-ˋˏ⛥┈ <b>{ping_msg["pong"]}</b> <code>{str(delta_ping_formatted).replace('.', ',')} ᴍs</code>
{tion}-ˋˏ⛥┈ <b>{ping_msg["owner"]}</b> <code>{client.me.mention}</code>
{yubot}-ˋˏ⛥┈ <b>{ping_msg["ubot"]}</b></blockquote>
"""
    else:
       _ping = f"""
<blockquote>-ˋˏ⛥┈ <b>{ping_msg["pong"]}</b> <code>{str(delta_ping_formatted).replace('.', ',')} ᴍs</code>
-ˋˏ⛥┈ <b>{ping_msg["owner"]}</b> <code>{client.me.mention}</code>
-ˋˏ⛥┈ <b>{ping_msg["ubot"]}</b></blockquote>
"""
    await message.reply(_ping)