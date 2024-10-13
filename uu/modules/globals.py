import asyncio

from pyrogram import *
from pyrogram.enums import *
from pyrogram.errors import *
from pyrogram.types import *

from config import Config

from uu import *


__MODULE__ = "Global"
__HELP__ = """
<b>Menu Globals</b>

<b>Global banned users!</b>
 <code>{0}gban</code>

<b>Global unbanned users!</b>
 <code>{0}ungban</code>
  
"""

      

@PY.UBOT("gban")
async def _(client, message):
    user_id = await extract_user(message)
    _msg = "<b>Processing...</b>"

    Tm = await message.reply(_msg)
    if not user_id:
        return await Tm.edit("<b>User not found!</b>")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await Tm.edit(error)
    done = 0
    failed = 0
    text = "<b>Global {}</b>\n\n<b>Succes: {} Chat</b>\n<b>Failed: {} chat</b>\n<b>User: <a href='tg://user?id={}'>{} {}</a></b>"
    global_id = await gcast_type(client, "global")
    for dialog in global_id:
        if user.id == Config.OWNER_ID:
            return await Tm.edit("<b>He is a developer!</b>")
        try:
            await client.ban_chat_member(dialog, user.id)
            done += 1
            await asyncio.sleep(0.1)
        except Exception:
            failed += 1
            await asyncio.sleep(0.1)
    await message.reply(
        text.format(
            "Banned", done, failed, user.id, user.first_name, (user.last_name or "")
        )
    )
    return await Tm.delete()


@PY.UBOT("ungban")
async def _(client, message):
    user_id = await extract_user(message)
    _msg = "<b>Processing...</b>"

    Tm = await message.reply(_msg)
    if not user_id:
        return await Tm.edit("<b>User not found!</b>")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await Tm.edit(error)
    done = 0
    failed = 0
    text = "<b>Global {}</b>\n\n<b>Succes: {} chat</b>\n<b>Failed: {} chat</b>\n<b>User: <a href='tg://user?id={}'>{} {}</a></b>"
    global_id = await gcast_type(client, "global")
    for dialog in global_id:
        try:
            await client.unban_chat_member(dialog, user.id)
            done += 1
            await asyncio.sleep(0.1)
        except Exception:
            failed += 1
            await asyncio.sleep(0.1)
    await message.reply(
        text.format(
            "Unbanned",
            done,
            failed,
            user.id,
            user.first_name,
            (user.last_name or ""),
        )
    )
    return await Tm.delete()
