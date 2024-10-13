import random
import re

from pyrogram import filters, Client
from asyncio import sleep
from re import search, IGNORECASE, escape


from uu import *

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from re import findall

from pyrogram import Client, filters
from pyrogram.types import ChatPermissions


__MODULE__ = "Auto Reply"
__HELP__ = """
<b>Menu Auto Reply!</b>

<b>Auto reply for group</b>(ultra)
 <code>{0}gcfilter [On or Off]</code>
 <code>{0}gcaddfilter [Name - Text/Reply]</code>
 <code>{0}gcdelfilter [Name]</code>
 <code>{0}gcfilters</code>

<b>Auto reply for private</b>(ultra)
 <code>{0}pvfilter [On or Off]</code>
 <code>{0}pvaddfilter [Name - Text/Reply]</code>
 <code>{0}pvdelfilter [Name]</code>
 <code>{0}pvfilters</code>   
  """


@PY.NO_CMD_UBOT("FILTERS_GC", TU)
async def _(client, message):
    try:
        chat_logs = TB.me.id
        all_filters = await DB.all_vars(client.me.id, "filters_gc") or {}

        for key, value in all_filters.items():
            if key == message.text.split()[0]:
                msg = await client.get_messages(int(chat_logs), int(value))
                return await msg.copy(message.chat.id, reply_to_message_id=message.id)
    except BaseException:
        pass


@PY.UBOT("gcfilter")
@PY.GROUP
@PY.ULTRA
async def _(client, message):
    txt = await message.reply(f"<b>Processing...</b>")
    arg = get_arg(message)

    if not arg or arg.lower() not in ["off", "on"]:
        return await txt.edit(f"<b>Type [on/off]</b>")

    type = True if arg.lower() == "on" else False
    await DB.set_vars(client.me.id, "filters_gc", type)
    return await txt.edit(f"<b>Successfully set to mode: {type}</b>")


@PY.UBOT("gcaddfilter")
@PY.GROUP
@PY.ULTRA
async def _(client, message):
    txt = await message.reply(f"<b> Processing...</b>")
    type, reply = type_and_msg(message)

    if not type and message.reply_to_message:
        return await txt.edit(f"<b>Reply text or enter text</b>")

    logs = TB.me.id
    if bool(logs):
        try:
            msg = await reply.copy(int(logs))
            await DB.set_vars(client.me.id, type, msg.id, "filters_gc")
            await txt.edit(f"<b>Message:</b> <code>{type}</code> <b>Successfully added to filter</b>")
        except Exception as error:
            await txt.edit(error)
    else:
        return await txt.edit(f"<b>Cannot create new a filter</b>")


@PY.UBOT("gcdelfilter")
@PY.GROUP
@PY.ULTRA
async def _(client, message):
    txt = await message.reply(f"<b>Processing..</b>")
    arg = get_arg(message)

    if not arg:
        return await txt.edit(f"<code>{message.text.split()[0]}</code> <b>Nama filter</b>")

    logs = TB.me.id
    all = await DB.all_vars(client.me.id, "filters_gc")

    if arg not in all:
        return await txt.edit(f"<b>Message:</b> <code>{arg}</code> <b>Not found!</b>")

    await DB.remove_vars(client.me.id, arg, "filters_gc")
    await client.delete_messages(logs, all[arg])
    return await txt.edit(f"<b>Message:</b> <code>{arg}</code> <b>Successfully removed to filter</b>")


@PY.UBOT("gcfilters")
@PY.GROUP
@PY.ULTRA
async def _(client, message):
    all_filters = await DB.all_vars(client.me.id, "filters_gc")
    if all_filters:
        msg = f"⛥ List filters\n"
        for x in all_filters.keys():
            msg += f" ├ {x}\n"
        msg += f" ╰ Total filters: {len(all_filters)}"
    else:
        msg = f" <b>Filters not found</b>"

    await message.reply(msg, quote=True)

