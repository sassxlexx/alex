import asyncio
import random

from gc import get_objects
from asyncio import sleep

from pyrogram.errors.exceptions import FloodWait

from uu import *


__MODULE__ = "Protect"
__HELP__ = """
<b>Menu Protect!</b>

<b>Enable or disable protect!</b>
 <code>{0}protect [on or off]</code>
  
<b>Adding word to list protect!</b>
 <code>{0}addword</code>
  
<b>Remove word from list protect!</b>
 <code>{0}delword</code>
  
<b>Get list word protect!</b>
 <code>{0}listword</code>
  
"""



@TU.on_message(filters.group & ~filters.me & ~filters.bot)
async def _(client, message):
    if await DB.get_vars(client.me.id, f"protect_{message.chat.id}"):
        word_split = message.text.split()
        word_list = await DB.get_vars(client.me.id, "word_protect") or []
        mention = (
            f"[{message.from_user.first_name} {message.from_user.last_name or ''}](tg://user?id={message.from_user.id})"
            if message.from_user
            else "."
        )
        for x in word_split:
            if x in word_list:
                try:
                    await message.delete()
                    msg = await message.reply(
                        f"{mention}, <b>Kata-kata anda terkena protect!</b>"
                    )
                    await asyncio.sleep(5)
                    return await msg.delete()
                except Exception:
                    pass



@PY.UBOT("protect")
@PY.GROUP
async def _(client, message):
    if len(message.command) < 2:
        return await message.reply(
            f"<b>Usage on or off!</b>"
        )

    query = {"on": True, "off": False}
    command = message.command[1].lower()

    if command not in query:
        return await message.reply(
            f"<code>{message.text.split()[0]}</code> <b>[ᴏɴ/ᴏғғ]</b>"
        )

    txt = (
        "<b>Protect has been successfully activated!</b>"
        if command == "on"
        else "<b>Protect has been successfully deactivated!</b>"
    )
    await DB.set_vars(client.me.id, f"protect_{message.chat.id}", query[command])
    await message.reply(txt)


@PY.UBOT("addword")
@PY.GROUP
async def _(client, message):
    vars = await DB.get_vars(client.me.id, "word_protect") or []
    text = get_arg(message).split()

    add_word = [x for x in text if x not in vars]
    vars.extend(add_word)
    await DB.set_vars(client.me.id, "word_protect", vars)

    if add_word:
        response = (
            f"<b>Successfully added the word to protect!</b>\n"
            f"<b>Added words:</b> {''.join(add_word)}"
        )
    else:
        response = "<b>No words added!</b>"

    return await message.reply(response)


@PY.UBOT("listword")
@PY.GROUP
async def _(client, message):
    vars = await DB.get_vars(client.me.id, "word_protect") or []
    if vars:
        msg = "<b>List Word!</b>\n\n"
        for x in vars:
            msg += f"{x}\n"
        msg += f"<b>\nTotal Word: {len(vars)}</b>"
    else:
        msg = "<b>No words!</b>"

    return await message.reply(msg, quote=True)


@PY.UBOT("delword")
@PY.GROUP
async def _(client, message):
    vars = await DB.get_vars(client.me.id, "word_protect") or []
    _, *text = get_arg(message).split()
    removed_list = [x for x in text if x in vars]
    vars = [x for x in vars if x not in removed_list]
    await DB.set_vars(client.me.id, "word_protect", vars)

    if removed_list:
        response = (
            f"<b>Successfully removed word from protect</b>\n"
            f"<b>Remove words:</b> {''.join(removed_list)}"
        )
    else:
        response = "<b>No words remove!</b>"

    return await message.reply(response)
