from pyrogram import *
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors.exceptions.not_acceptable_406 import ChannelPrivate

from uu import *

__MODULE__ = "Join & Leave"
__HELP__ = """
<b>Menu Join & Leave!!</b>

<b>Leave in the group!</b>
 <code>{0}kickme</code>

<b>Join the group!</b>
 <code>{0}join</code>

<b>Leave all the group!</b>(ultra)
 <code>{0}leaveallgc</code>

<b>Leave all the channel!</b>(ultra)
 <code>{0}leaveallch</code>

<b>Leave all group restricted you!</b>(ultra)
 <code>{0}leaveallmute</code>
"""


@PY.UBOT("kickme")
@PY.GROUP
async def _(client, message):
    if len(message.command) > 1:
        input_identifier = message.command[1]
    else:
        input_identifier = message.chat.id
    
    chat_id = await extract_id(message, input_identifier)
    try:
        await message.reply(f"<b>Good Bye!!</b>")
        await client.leave_chat(chat_id)
    except Exception as ex:
        await message.reply(f"<b>Error:</b>{str(ex)}")



@PY.UBOT("join")
async def _(client, message):
    if len(message.command) > 1:
        input_identifier = message.command[1]
    else:
        return await message.reply("<b>Please provide a username or ID!</b>")
    
    chat_id = await extract_id(message, input_identifier)
    if not chat_id:
        return await message.reply("<b>Invalid id!</b>")
    try:
        await message.reply(f"<b>Succes joining in group chat:</b>{chat_id}")
        await client.join_chat(chat_id)
    except Exception as ex:
        await message.reply(f"<b>Error:</b>{str(ex)}")


@PY.UBOT("leaveallgc")
@PY.ULTRA
async def _(client, message):
    Tk = await message.reply(f"<b>Leaving all group...</b>")
    er = 0
    done = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            chat = dialog.chat.id
            try:
                done += 1
                await client.leave_chat(chat)
            except BaseException:
                er += 1
    await Tk.edit(
        f"<b>Succes leave group chat!!\ndone: <code>{done}</code> group\nfailed: <code>{er}</code> group</b>"
    )


@PY.UBOT("leaveallch")
@PY.ULTRA
async def _(client, message):
    Tk = await message.reply(f"<b>Leaving all group...</b>")
    er = 0
    done = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.CHANNEL):
            chat = dialog.chat.id
            try:
                done += 1
                await client.leave_chat(chat)
            except BaseException:
                er += 1
    await Tk.edit(
        f"<b>Succes leave group chat!!\ndone: <code>{done}</code> group\nfailed: <code>{er}</code> group</b>"
    )

@PY.UBOT("leaveallmute")
@PY.ULTRA
async def _(client, message):
    done = 0
    Tk = await message.reply(f"<b>Processing...</b>")
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            chat = dialog.chat.id
            try:
                member = await client.get_chat_member(chat, "me")
                if member.status == ChatMemberStatus.RESTRICTED:
                    await client.leave_chat(chat)
                    done += 1
            except Exception:
                pass
    await Tk.edit(f"<b>Succes Leave {done} Group Muted!!</b>")
