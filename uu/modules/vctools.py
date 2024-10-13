import asyncio
from random import randint

from pytgcalls.types import *
from pytgcalls.exceptions import *
from youtubesearchpython import VideosSearch

from pyrogram import *
from pyrogram.types import *
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.types import InputPeerChannel, InputPeerChat
from pyrogram.errors import FloodWait, MessageNotModified

from uu import *


__MODULE__ = "Vc Tools"
__HELP__ = """
<b>Menu Vc Tools!</b>

<b>Start group calls!</b>
 <code>{0}startvc</code>

<b>End group calls</b>
 <code>{0}stopvc</code>

<b>Joining group calls!</b>
 <code>{0}joinvc</code>

<b>Leaving group calls!</b>
 <code>{0}leavevc</code>
"""

async def get_group_call(client, message):
    chat_peer = await client.resolve_peer(message.chat.id)
    if isinstance(chat_peer, (InputPeerChannel, InputPeerChat)):
        if isinstance(chat_peer, InputPeerChannel):
            full_chat = (
                await client.invoke(GetFullChannel(channel=chat_peer))
            ).full_chat
        elif isinstance(chat_peer, InputPeerChat):
            full_chat = (
                await client.invoke(GetFullChat(chat_id=chat_peer.chat_id))
            ).full_chat
        if full_chat is not None:
            return full_chat.call
    await message.reply("<b>ɴᴏ ɢʀᴏᴜᴘ ᴄᴀʟʟ</b>")
    return False



@PY.UBOT("jvc")
@PY.OWNER
async def _(clients, message):
    if len(message.command) > 1:
        input_identifier = message.command[1]
    else:
        input_identifier = message.chat.id

    chat_id = await extract_id(message, input_identifier)
    if not chat_id:
        return await message.reply("<b>Invalid id!</b>")

    error_messages = []
    for x_ in TU._ubot:
        try:
            a_calls = await x_.call_py.calls
            if_chat = a_calls.get(chat_id)
            if if_chat:
                error_messages.append(f"<b>Id: {x_.name}\nReason: Already on group calls!</b>")
                continue

            await x_.call_py.play(chat_id)
            await x_.call_py.mute_stream(chat_id)

        except NoActiveGroupCall:
            error_messages.append(f"<b>Id: {x_.name}\nReason: No voice chat in the group!</b>")
        except Exception as e:
            error_messages.append(f"<b>Id: {x_.name}\nError:</b>{e}\n")

    if error_messages:
        x = await message.reply("\n".join(error_messages))
        await asyncio.sleep(3)
        return await x.edit("<b>All clients joined in group calls!</b>")
    else:
        await message.reply("<b>All clients joined in group calls!</b>")


@PY.UBOT("lvc")
@PY.OWNER
async def _(clients, message):
    if len(message.command) > 1:
        input_identifier = message.command[1]
    else:
        input_identifier = message.chat.id

    chat_id = await extract_id(message, input_identifier)
    if not chat_id:
        return await message.reply("<b>Invalid id!</b>")

    error_messages = []
    for x_ in TU._ubot:
        try:
            await x_.call_py.leave_call(chat_id)
        except GroupCallNotFound:
            error_messages.append(f"<b>Id: {x_.name}\nReason: Not currently in group calls!</b>")
        except Exception as e:
            error_messages.append(f"<b>Id: {x_.name}\nError:</b>{e}\n")

    if error_messages:
        x = await message.reply("\n".join(error_messages))
        await asyncio.sleep(3)
        return await x.edit("<b>All clients leave in group calls!</b>")
    else:
        await message.reply("<b>All clients leave in group calls!</b>")


@PY.UBOT("startvc")
@PY.GROUP
async def _(client, message):
    flags = " ".join(message.command[1:])
    _msg = "<b>Processing...</b>"

    msg = await message.reply(_msg)
    vctitle = get_arg(message)
    chat_id = message.chat.title if flags == ChatType.CHANNEL else message.chat.id

    args = f"<b>Active voice chat!\nChat:</b> {chat_id}"

    try:
        if vctitle:
            args += f"\n<b>Title:</b>  {vctitle}"

        await client.invoke(
            CreateGroupCall(
                peer=(await client.resolve_peer(chat_id)),
                random_id=randint(10000, 999999999),
                title=vctitle if vctitle else None,
            )
        )
        await msg.edit(args)
    except Exception as e:
        await msg.edit(f"INFO: {e}")


@PY.UBOT("stopvc")
@PY.GROUP
async def _(client, message):
    _msg = "<b>Processing...</b>"

    msg = await message.reply(_msg)
    group_call = await get_group_call(client, message)

    if not group_call:
        return await msg.edit("<b>No active voice chat!</b>")

    await client.invoke(DiscardGroupCall(call=group_call))
    await msg.edit(
        f"<b>Voice chat ends!\nChat:</b> {message.chat.title}"
    )



@PY.UBOT("joinvc")
async def _(client, message):
    if len(message.command) > 1:
        input_identifier = message.command[1]
    else:
        input_identifier = message.chat.id

    chat_id = await extract_id(message, input_identifier)
    a_calls = await client.call_py.calls
    if_chat = a_calls.get(chat_id)
    if not chat_id:
        return await message.reply("<b>Invalid id!</b>")
    if if_chat:
        return await message.reply("<b>Already on voice chat</b>")
    try:
        await client.call_py.play(chat_id)
        await client.call_py.mute_stream(chat_id)
        return await message.reply("<b>Successfully joined voice chat</b>")
    except NoActiveGroupCall:
        return await message.reply("<b>There is no voice chat in the group!</b>")
    except Exception as e:
        return await message.reply(f"<b>Error:</b> {e}")


@PY.UBOT("leavevc")
async def _(client, message):
    if len(message.command) > 1:
        input_identifier = message.command[1]
    else:
        input_identifier = message.chat.id

    chat_id = await extract_id(message, input_identifier)
    if not chat_id:
        return await message.reply("<b>Invalid id!</b>")
    try:
        await client.call_py.leave_call(chat_id)
        return await message.reply(f"<b>Successfully leave voice chat</b>")
    except GroupCallNotFound:
        return await message.reply("<b>Not currently in voice chat!</b>")
    except Exception as e:
        return await message.reply(f"<b>Error:</b> {e}")







