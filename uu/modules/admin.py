import asyncio

from pyrogram import *
from pyrogram.enums import *
from pyrogram.errors import *
from pyrogram.types import *
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    ChatNotModified,
)

from uu import *


__MODULE__ = "Admin"
__HELP__ = """
<b>Menu Admins</b>

<b>Set your group pic!</b>
 <code>{0}setpic</code>

<b>Pinned or unpinned message in group chat!</b>
 <code>{0}pin or {0}unpin</code>

<b>Lock or unlock permissions!</b>
 <code>{0}lock or {0}unlock</code>

<b>List permissions</b>
 <code>{0}locks</code>

<b>Banned members in group!</b>
 <code>{0}ban or {0}dban</code>

<b>Unbanned members in group!</b>
 <code>{0}unban</code>

<b>Muted members in group!</b>
 <code>{0}mute</code>

<b>Unmuted members in group!</b>
 <code>{0}unmute</code>

<b>Kicked members in group!</b>
 <code>{0}kick or {0}dkick</code>

<b>Warnings to user!</b>(ultra)
 <code>{0}warn or {0}dwarn</code>

<b>Settings warnings!</b>(ultra)
 <code>{0}setwarn [Number] [Kick/Mute/Ban]</code>

<b>Cleaning ghost account in group!</b>(ultra)
 <code>{0}zombies</code>
"""


unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=False,
    can_send_polls=False,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)


DEVS = [
        5654247585, # uu
    ]


data = {
    "msg": "can_send_messages",
    "stickers": "can_send_other_messages",
    "gifs": "can_send_other_messages",
    "media": "can_send_media_messages",
    "games": "can_send_other_messages",
    "inline": "can_send_other_messages",
    "url": "can_add_web_page_previews",
    "polls": "can_send_polls",
    "info": "can_change_info",
    "invite": "can_invite_users",
    "pin": "can_pin_messages",
}


async def current_chat_permissions(client, chat_id):
    perms = []
    perm = (await client.get_chat(chat_id)).permissions
    if perm.can_send_messages:
        perms.append("can_send_messages")
    if perm.can_send_media_messages:
        perms.append("can_send_media_messages")
    if perm.can_send_other_messages:
        perms.append("can_send_other_messages")
    if perm.can_add_web_page_previews:
        perms.append("can_add_web_page_previews")
    if perm.can_send_polls:
        perms.append("can_send_polls")
    if perm.can_change_info:
        perms.append("can_change_info")
    if perm.can_invite_users:
        perms.append("can_invite_users")
    if perm.can_pin_messages:
        perms.append("can_pin_messages")
    return perms


async def tg_lock(
    client,
    message,
    parameter,
    permissions: list,
    perm: str,
    lock: bool,
):
    if lock:
        if perm not in permissions:
            return await message.reply(f"`{parameter}` <b>Already locks!</b>")
        permissions.remove(perm)
    else:
        if perm in permissions:
            return await message.reply(f"`{parameter}` <b>Already unlock!</b>")
        permissions.append(perm)
    permissions = {perm: True for perm in set(permissions)}
    try:
        await client.set_chat_permissions(
            message.chat.id, ChatPermissions(**permissions)
        )
    except ChatNotModified:
        return await message.reply(
            f"<code>{message.text.split()[0]}</code> <b>Type!</b>"
        )
    except ChatAdminRequired:
        return await message.reply("<b>Doesn't have permission!</b>")
    await message.reply(
        (
            f"<b>Locks permissions!\nType: <code>{parameter}</code>\nGroup: {message.chat.title}</b>"
            if lock
            else f"<b>Unlock permissions!\nType: <code>{parameter}</code>\nGroup: {message.chat.title}</b>"
        )
    )


@PY.UBOT("lock|unlock")
@PY.GROUP
async def _(client, message):
    if len(message.command) != 2:
        return await message.reply(f"<code>{message.text.split()[0]}</code> <b>Type!</b>")
    chat_id = message.chat.id
    parameter = message.text.strip().split(None, 1)[1].lower()
    state = message.command[0].lower()
    if parameter not in data and parameter != "all":
        return await message.reply(incorrect_parameters)
    permissions = await current_chat_permissions(client, chat_id)
    if parameter in data:
        await tg_lock(
            client,
            message,
            parameter,
            permissions,
            data[parameter],
            bool(state == "lock"),
        )
    elif parameter == "all" and state == "lock":
        try:
            await client.set_chat_permissions(chat_id, ChatPermissions())
            await message.reply(
                f"<b>Lock permissions!\nType: <code>{parameter}</code>\nGroup: {message.chat.title}</b>"
            )
        except ChatAdminRequired:
            return await message.reply("<b>Doesn't have permission!</b>")
        except ChatNotModified:
            return await message.reply(
                f"<b>Locks permissions!\nType: <code>{parameter}</code>\nGroup: {message.chat.title}</b>"
            )
    elif parameter == "all" and state == "unlock":
        try:
            await client.set_chat_permissions(
                chat_id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True,
                    can_send_polls=True,
                    can_change_info=False,
                    can_invite_users=True,
                    can_pin_messages=False,
                ),
            )
        except ChatAdminRequired:
            return await message.reply("<b>Doesn't have permission!</b>")
        await message.reply(
            f"<b>Unlock permissions!\nType: <code>{parameter}</code>\nGroup: {message.chat.title}</b>"
        )


@PY.UBOT("locks")
@PY.GROUP
async def _(client, message):
    permissions = await current_chat_permissions(client, message.chat.id)
    if not permissions:
        return await message.reply("<b>Lock all!</b>")

    perms = " -> __**" + "\n -> __**".join(permissions) + "**__"
    await message.reply(perms)

@PY.UBOT("setgpic")
@PY.GROUP
async def _(client, message):
    xx = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    can_change_admin = xx.can_change_info
    can_change_member = message.chat.permissions.can_change_info
    if not (can_change_admin or can_change_member):
        await message.reply("<b>You don't have enough permission</b>")
    if message.reply_to_message:
        if message.reply_to_message.photo:
            await client.set_chat_photo(
                message.chat.id, photo=message.reply_to_message.photo.file_id
            )
            return
    else:
        await message.reply("<b>Reply to a photo to set it !</b>")


@PY.UBOT("pin|unpin")
@PY.GROUP
async def _(client, message):
    Tk = await message.reply("<b>Processing...</b>")
    if not message.reply_to_message:
        return await Tk.edit("<b>Reply to a message to pin/unpin it.</b>")
    if client.me.id not in await list_admins(client, message.chat.id):
        return await Tk.edit("<b>I don't have enough permissions!</b>")
    r = message.reply_to_message
    if message.command[0][0] == "u":
        await r.unpin()
        return await Tk.edit(
            f"<b>Unpinned [this]({r.link}) message.</b>",
            disable_web_page_preview=True,
        )
    await r.pin(disable_notification=True)
    await Tk.edit(
        f"<b>Pinned [this]({r.link}) message.</b>",
        disable_web_page_preview=True,
    )


@PY.UBOT("ban|dban")
@PY.GROUP
async def _(client, message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    if client.me.id not in await list_admins(client, message.chat.id):
        return await message.reply("<b>I don't have enough permissions!</b>")
    if not user_id:
        return await message.reply("<b>I can't find that user!</b>")
    if user_id == client.me.id:
        return await message.reply("<b>I can't ban myself!</b>")
    if user_id in DEVS:
        return await message.reply("<b>I can't ban my developer!</b>")
    if user_id in (await list_admins(client, message.chat.id)):
        return await message.reply("<b>I can't ban an admin!!</b>")
    try:
        mention = (await client.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )
    msg = f"""
<b>Banned user:</b> {mention}
<b>Banned by:</b> {message.from_user.mention if message.from_user else 'Anon'}
"""
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msg += f"<b>Reason:</b> {reason}"
    await message.chat.ban_member(user_id)
    await message.reply(msg)


@PY.UBOT("unban")
@PY.GROUP
async def _(client, message):
    reply = message.reply_to_message
    if client.me.id not in await list_admins(client, message.chat.id):
        return await message.reply("<b>I don't have enough permissions!</b>")
    if reply and reply.sender_chat and reply.sender_chat != message.chat.id:
        return await message.reply("<b>You cannot unban a channel!</b>")

    if len(message.command) == 2:
        user = message.text.split(None, 1)[1]
    elif len(message.command) == 1 and reply:
        user = message.reply_to_message.from_user.id
    else:
        return await message.reply(
            "<b>Provide a username or reply to a user's message to unban!</b>"
        )
    await message.chat.unban_member(user)
    umention = (await client.get_users(user)).mention
    await message.reply(f"<b>Unbanned!</b> {umention}")


@PY.UBOT("mute")
@PY.GROUP
async def _(client, message):
    user_id, reason = await extract_user_and_reason(message)
    if client.me.id not in await list_admins(client, message.chat.id):
        return await message.reply("<b>I don't have enough permissions!</b>")
    if not user_id:
        return await message.reply("<b>I can't find that user!</b>")
    if user_id == client.me.id:
        return await message.reply("<b>I can't mute myself!</b>")
    if user_id in DEVS:
        return await message.reply("<b>I can't mute my developer!</b>")
    if user_id in (await list_admins(client, message.chat.id)):
        return await message.reply("<b>I can't mute an admin!</b>")
    mention = (await client.get_users(user_id)).mention
    msg = f"""
<b>Muted user:</b> {mention}
<b>Muted by:</b> {message.from_user.mention if message.from_user else 'Anon'}
"""
    if reason:
        msg += f"<b>Reason:</b> {reason}"
    await message.chat.restrict_member(user_id, permissions=ChatPermissions())
    await message.reply(msg)


@PY.UBOT("unmute")
@PY.GROUP
async def _(client: Client, message: Message):
    user_id = await extract_user(message)
    if client.me.id not in await list_admins(client, message.chat.id):
        return await message.reply("<b>I don't have enough permissions!</b>")
    if not user_id:
        return await message.reply("<b>I can't find that user.</b>")
    await message.chat.restrict_member(user_id, permissions=unmute_permissions)
    umention = (await client.get_users(user_id)).mention
    await message.reply(f"<b>Unmuted!</b> {umention}")


@PY.UBOT("kick|dkick")
@PY.GROUP
async def _(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    if client.me.id not in await list_admins(client, message.chat.id):
        return await message.reply("<b>I don't have enough permissions!</b>")
    if not user_id:
        return await message.reply("<b>I can't find that user!</b>")
    if user_id == client.me.id:
        return await message.reply("<b>I can't kick myself!</b>")
    if user_id == DEVS:
        return await message.reply("<b>I can't kick my developer!</b>")
    if user_id in (await list_admins(client, message.chat.id)):
        return await message.reply("<b>I can't kick an admin, You know the rules, so do i!</b>")
    mention = (await client.get_users(user_id)).mention
    msg = f"""
<b>Kicked user:</b> {mention}
<b>Kicked by:</b> {message.from_user.mention if message.from_user else 'Anon'}"""
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msg += f"\n<b>Reason:</b> {reason}"
    try:
        await message.chat.ban_member(user_id)
        await message.reply(msg)
        await asyncio.sleep(1)
        await message.chat.unban_member(user_id)
    except ChatAdminRequired:
        return await message.reply("<b>I don't have enough permissions!</b>")


@PY.UBOT("warn|dwarn")
@PY.ULTRA
@PY.GROUP
async def _(client, message):
    user_id, reason = await extract_user_and_reason(message)
    if client.me.id not in await list_admins(client, message.chat.id):
        return await message.reply("<b>I don't have enough permissions!</b>")
    if not user_id:
        return await message.reply("<b>I can't find that user!</b>")
    if user_id == client.me.id:
        return await message.reply("<b>I can't warn myself!</b>")
    if user_id in DEVS:
        return await message.reply("<b>I can't warn my developer!</b>")
    if user_id in (await list_admins(client, message.chat.id)):
        return await message.reply("<b>I can't warn an admin!</b>")

    current_warnings = await DB.add_warn(user_id)
    limit = await DB.get_warn_limit(client.me.id)
    limit_user = await DB.get_warn(user_id)
    action_type = await DB.get_action(client.me.id)
    mention = (await client.get_users(user_id)).mention
  
    msg = f"""
<b>Warn user:</b> {mention}
<b>Warn by:</b> {message.from_user.mention if message.from_user else 'Anon'}
<b>Warn limit:</b> {limit_user}/{limit}
"""
    if reason:
        msg += f"<b>Reason:</b> {reason}"

    if message.command[0][0] == "d":
        await message.reply_to_message.delete()

    if current_warnings >= limit:
        if action_type == "mute":
            await message.chat.restrict_member(user_id, permissions=ChatPermissions())
            await DB.reset_warn(user_id)
            return await message.reply("<b>Muted the user because the warning limit has been reached!</b>")
        elif action_type == "kick":
            await message.chat.ban_member(user_id)
            await asyncio.sleep(1)
            await message.chat.unban_member(user_id)
            await DB.reset_warn(user_id)
            return await message.reply("<b>Kicked the user because the warning limit has been reached!</b>")
        elif action_type == "ban":
            await message.chat.ban_member(user_id)
            await DB.reset_warn(user_id)
            return await message.reply("<b>Banned the user because the warning limit has been reached!</b>")

    await message.reply(msg)


@PY.UBOT("setwarn")
@PY.ULTRA
async def _(client, message):
    arg = get_arg(message)
    if not arg:
        return await message.reply("<b>Please provide the limit and action!</b>")
        
    try:
        limit, action = arg.split(" ", 1)
        limit = int(limit)
        if action not in ["kick", "mute", "ban"]:
            return await message.reply("<b>Invalid action. Choose from 'kick', 'mute', or 'ban'!</b>")

        await DB.set_warn_limit(client.me.id, limit)
        await DB.set_action(client.me.id, action)
        await message.reply(f"<b>Warning limit set to {limit} with action '{action}'!</b>")
    except ValueError:
        await message.reply("<b>Invalid format!</b>")


@PY.UBOT("zombies")
@PY.GROUP
@PY.ULTRA
async def _(client, message):
    chat_id = message.chat.id
    deleted_users = []
    banned_users = 0
    try:
        async for i in client.get_chat_members(chat_id):
            if i.user.is_deleted:
                deleted_users.append(i.user.id)
        if len(deleted_users) > 0:
            for deleted_user in deleted_users:
                try:
                    banned_users += 1
                    await message.chat.ban_member(deleted_user)
                except Exception as e:
                    await message.reply(f"<b>Error: Telegram says: [400 MESSAGE_ID_INVALID]</b>")
            await message.reply(f"<b>Successfully kicked {banned_users} deleted account(s)</b>")
        else:
            await message.reply("<b>There isn't any!!</b>")
    except Exception as ex:
        await message.reply(f"<b>Error: Telegram says: [400 MESSAGE_NOT_MODIFIED]</b>")

