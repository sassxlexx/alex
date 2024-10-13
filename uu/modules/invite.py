import asyncio

from pyrogram import Client, filters
from pyrogram.enums import ChatType, UserStatus
from pyrogram.types import Message

from uu import *


__MODULE__ = "Inviting"
__HELP__ = """
<b>Menu Inviting!</b>

<b>Added members to group!</b>
 <code>{0}invite</code>

<b>Inviting all members from group</b>
 <code>{0}inviteall</code>

<b>Getting invite link group</b>
 <code>{0}invitelink</code>
"""


@PY.UBOT("invite")
@PY.GROUP
async def _(client, message):
    Tk = await message.reply("<b>Adding Users!</b>")

    if len(message.command) < 2:
        return await Tk.edit("<b>Give Me Users To Add!</b>")

    user_s_to_add = message.command[1]
    user_list = user_s_to_add.split(" ")

    try:
        await client.add_chat_members(message.chat.id, user_list)
    except Exception as e:
        return await Tk.edit(f"<b>Unable To Add Users! Error: {str(e)}</b>")

    await Tk.edit(f"<b>Successfully Added</b> {len(user_list)} <b>Users</b>")
    

@PY.UBOT("inviteall")
@PY.GROUP
async def _(client, message):
    Tk = await message.reply("<b>Processing...</b>")
    text = message.text.split(" ", 1)
    queryy = text[1]
    chat = await client.get_chat(queryy)
    tgchat = message.chat
    if not queryy:
        await Tk.edit("<b>Invalid inviting!</b>")
    else:
        await Tk.edit(f"<b>inviting users from</b> {chat.title}")
    async for member in client.get_chat_members(chat.id):
        user = member.user
        zxb = [
            UserStatus.ONLINE,
            UserStatus.OFFLINE,
            UserStatus.RECENTLY,
            UserStatus.LAST_WEEK,
        ]
        if user.status in zxb:
            try:
                await client.add_chat_members(tgchat.id, user.id)
            except Exception as e:
                await Tk.edit(f"<b>Error:<b> {e}")


@PY.UBOT("invitelink")
@PY.GROUP
async def _(client, message):
    Tk = await message.reply("<b>Processing...</b>")
    if message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        message.chat.title
        try:
            link = await client.export_chat_invite_link(message.chat.id)
            await Tk.edit(f"<b>Link Invite:</b> {link}")
        except Exception:
            await Tk.edit("<b>Denied permission!</b>")
