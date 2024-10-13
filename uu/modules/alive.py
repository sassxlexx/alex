import os

from config import Config 
from datetime import datetime
from time import time

from pyrogram.raw.functions import Ping
from pyrogram.types import *

from uu import *


@PY.UBOT("alive")
async def _(client, message):
    try:
        x = await client.get_inline_bot_results(
            TB.me.username, f"alive {message.id} {client.me.id}"
        )
        await message.reply_inline_bot_result(x.query_id, x.results[0].id, quote=True)
    except Exception as error:
        await message.reply(error)


@PY.INLINE("^alive")
async def _(client, inline_query):
    get_id = inline_query.query.split()
    for my in TU._ubot:
        if int(get_id[2]) == my.me.id:
            try:
                peer = my._get_my_peer[my.me.id]
                users = len(peer["pm"])
                group = len(peer["gc"])
            except Exception:
                users = random.randrange(await my.get_dialogs_count())
                group = random.randrange(await my.get_dialogs_count())
            get_exp = await DB.get_expired(my.me.id)
            exp = get_exp.strftime("%d-%m-%Y") if get_exp else "None"
            if my.me.id == Config.OWNER_ID:
                status = "__Owner__"
            elif my.me.id in await DB.get_list_vars(client.me.id, "seller_users"):
                status = "__Admin__"
            else:
                status = ""
            if await DB.get_vars(my.me.id, "ultrapremium"):
                type = "Ultrapremium"
            else:
                type = "Premium"
            button = BTN.ALIVE(get_id)
            start = datetime.now()
            await my.invoke(Ping(ping_id=0))
            ping = (datetime.now() - start).microseconds / 1000
            uptime = await get_time((time() - start_time))
            msg = f"""
<b>{TB.me.mention}
    status: {type} {status}
      dc_id: <code>{my.me.dc_id}</code>
      ping_dc: <code>{ping} ms</code>
      expired: <code>{exp}</code> 
      peer_group: <code>{group}</code>
      peer_users: <code>{users}</code>
      ubot_uptime: <code>{uptime}</code></b>
"""
            await client.answer_inline_query(
                inline_query.id,
                cache_time=0,
                results=[
                    (
                        InlineQueryResultArticle(
                            title="💬",
                            reply_markup=InlineKeyboardMarkup(button),
                            input_message_content=InputTextMessageContent(msg),
                        )
                    )
                ],
            )


@PY.CALLBACK("alv_cls")
async def _(client, callback_query):
    data_parts = callback_query.data.split()
    if len(data_parts) < 3:
        return
    user_id = int(data_parts[2])
    if callback_query.from_user.id != user_id:
        return
    unpacked_message = unpackInlineMessage(callback_query.inline_message_id)
    for bot in TU._ubot:
        if callback_query.from_user.id == int(bot.me.id):
            await bot.delete_messages(
                unpacked_message.chat_id, 
                [int(data_parts[1]), unpacked_message.message_id]
            )
