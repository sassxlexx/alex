import asyncio
import random

from config import Config
from gc import get_objects
from asyncio import sleep

from pyrogram import *
from pyrogram.enums import *
from pyrogram.raw.functions.messages import DeleteHistory, StartBot
from pyrogram.errors.exceptions import FloodWait

from uu import *


__MODULE__ = "Broadcast"
__HELP__ = """
<b>Menu Broadcasting!</b>

<b>Type broadcast!</b>
 <code>'all'</code> , mengirim ke users and group
 <code>'group'</code> , mengirim ke group
 <code>'users'</code> , mengirim ke pengguna
 <code>'db'</code> , mengirim ke db

<b>Global sending message!</b>
 <code>{0}gcast [Text/Reply]</code>
 <code>{0}bc [Type] [Text/reply]</code>

<b>Cancelled global sending message</b>
 <code>{0}cancelbc or {0}cancelgcast</code>

<b>Checking account limits</b>
 <code>{0}limit</code>

<b>Adding to blakclist!</b>
 <code>{0}addbl or {0}blbc</code>

<b>Removing from blacklist!</b>
 <code>{0}unbl</code>

<b>Remove all from blacklist!</b>
 <code>{0}delallbl</code>

<b>Getting blacklist!</b>
 <code>{0}listbl</code>

<b>Adding to data broadcast</b>(ultra)
 <code>{0}addbcdb</code> or {0}bcdb</code>

<b>Removing from data broadcast</b>(ultra)
 <code>{0}unbcdb</code>

<b>Remove all from broadcast db</b>(ultra)
 <code>{0}delallbcdb</code>

<b>Getting data broadcast</b>(ultra)
 <code>{0}listbcdb</code>

<b>Query AutoGcast</b>
 <code>'on/off'</code> , mengaktifkan/menonaktifkan
 <code>'text'</code> , mengatur pesan [text]
 <code>'delay'</code> , mengatur waktu pesan [angka]
 <code>'limit'</code> , mengaktifkan limit [on/off]
 <code>'remove'</code> , mereset pesan [angka/all]
 <code>'list'</code> , melihat daftar pesan text

<b>Automatically send messages to group</b>
<code>{0}autogcast [query]</code>

"""


async def limit_cmd(client, message):
    await client.unblock_user("SpamBot")
    bot_info = await client.resolve_peer("SpamBot")
    response = await client.invoke(
        StartBot(
            bot=bot_info,
            peer=bot_info,
            random_id=client.rnd_id(),
            start_param="start",
        )
    )
    await sleep(1)
    status = await client.get_messages("SpamBot", response.updates[1].message.id + 1)
    await status.copy(message.chat.id, reply_to_message_id=message.id)
    return await client.invoke(DeleteHistory(peer=bot_info, max_id=0, revoke=True))


@PY.UBOT("limit")
async def _(client, message):
    await client.unblock_user("SpamBot")
    bot_info = await client.resolve_peer("SpamBot")
    _msg = "<b>Processing...</b>"

    msg = await message.reply(_msg)
    response = await client.invoke(
        StartBot(
            bot=bot_info,
            peer=bot_info,
            random_id=client.rnd_id(),
            start_param="start",
        )
    )
    await sleep(1)
    await msg.delete()
    status = await client.get_messages("SpamBot", response.updates[1].message.id + 1)
    await status.copy(message.chat.id, reply_to_message_id=message.id)
    return await client.invoke(DeleteHistory(peer=bot_info, max_id=0, revoke=True))


@PY.BOT("broadcast")
@PY.OWNER
async def _(client, message):
    msg = await message.reply("<b>Processing...</b>", quote=True)

    send = get_message(message)
    if not send:
        return await msg.edit("<b>Mohon balas sesuatu...</b>")

    susers = await DB.get_list_vars(client.me.id, "saved_users")
    done = 0
    for chat_id in susers:
        try:
            if message.reply_to_message:
                await send.forward(chat_id)
            else:
                await client.send_message(chat_id, send)
            done += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            if message.reply_to_message:
                await send.forward(chat_id)
            else:
                await client.send_message(chat_id, send)
            done += 1
        except Exception:
            pass

    return await msg.edit(f"<b>Pesan broadcast berhasil terkirim ke {done} user</b>")



broadcasts = []

@PY.UBOT("gcast")
async def broadcast_speed(client, message):
    broadcasts.append(client.me.id)
    send = get_message(message)
    gcs = await message.reply("<b>Start the broadcast process...</b>")
    if not send:
        await gcs.edit(f"<b>Type invalid!</b>")
        broadcasts.remove(client.me.id)
        return
    chats = await gcast_type(client, "group")
    blacklist = await DB.get_list_vars(client.me.id, "blacklist")
    done = 0
    failed = 0
    for chat_id in chats:
        if chat_id in blacklist:
            continue
        try:
            if client.me.id not in broadcasts:
                break
            if message.reply_to_message:
                await send.copy(chat_id)
            else:
                await client.send_message(chat_id, send)
            done += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            if message.reply_to_message:
                await send.copy(chat_id)
            else:
                await client.send_message(chat_id, send)
            done += 1
            if client.me.id not in broadcasts:
                break
        except Exception:
            failed += 1
            pass

    if client.me.id not in broadcasts:
        await gcs.delete()
        _gcs = f"""
<b>Broadcast Cancelled!!</b>

<b>Type:</b> group
<b>Done:</b> {done} chat
<b>Failed:</b> {failed} chat
"""
        await message.reply(_gcs)
    else:
        broadcasts.remove(client.me.id)
        await gcs.delete()
        _gcs = f"""
<b>Broadcast Completed!!</b>

<b>Type:</b> group
<b>Done:</b> {done} chat
<b>Failed:</b> {failed} chat
"""
        await message.reply(_gcs)


@PY.UBOT("bc")
async def _(client, message):
    broadcasts.append(client.me.id)

    gcs = await message.reply("<b>Start the broadcast process...</b>")

    command, text = type_and_msg(message)
    if command not in ["group", "users", "all", "db"] or not text:
        broadcasts.remove(client.me.id)
        return await gcs.edit(f"<b>Type invalid!</b>")

    chats = await gcast_type(client, command)
    bl = await DB.get_list_vars(client.me.id, "blacklist")

    done = 0
    failed = 0

    for chat_id in chats:
        if chat_id in await DB.get_list_vars(client.me.id, "bcdb_users"):
            if command not in "db":
                continue
            else:
                try:
                    if client.me.id not in broadcasts:
                        break
                    await (text.copy(chat_id) if message.reply_to_message else client.send_message(chat_id, text))
                    done += 1
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    print(f"[Kanaeru]: {str(e)}")
                    if client.me.id not in broadcasts:
                        break
                    await (text.copy(chat_id) if message.reply_to_message else client.send_message(chat_id, text))
                    done += 1
                except Exception as e:
                    failed += 1
                    print(f"[Kanaeru]: {str(e)}")
                    pass
        if chat_id in bl:
            continue
        try:
            if client.me.id not in broadcasts:
                break
            await (text.copy(chat_id) if message.reply_to_message else client.send_message(chat_id, text))
            done += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            print(f"[Kanaeru]: {str(e)}")
            if client.me.id not in broadcasts:
                break
            await (text.copy(chat_id) if message.reply_to_message else client.send_message(chat_id, text))
            done += 1
        except Exception as e:
            failed += 1
            print(f"[Kanaeru]: {str(e)}")
            pass

    
    if client.me.id not in broadcasts:
        await gcs.delete()
        _gcs = f"""
<b>Broadcast Cancelled!!</b>

<b>Type:</b> {command}
<b>Done:</b> {done} chat
<b>Failed:</b> {failed} chat
"""
        await message.reply(_gcs)
    else:
        broadcasts.remove(client.me.id)
        await gcs.delete()
        _gcs = f"""
<b>Broadcast Completed!!</b>

<b>Type:</b> {command}
<b>Done:</b> {done} chat
<b>Failed:</b> {failed} chat
"""
        await message.reply(_gcs)
    


@PY.UBOT("cancelbc|cancelgcast")
async def _(client, message):
    if client.me.id not in broadcasts:
        return await message.reply(
            "<b>Not currently broadcasting!</b>"
        )
    try:
        broadcasts.remove(client.me.id)
    except Exception:
        pass
    await message.reply("<b>Broadcast successfully cancelled!</b>")


@PY.UBOT("addbcdb|bcdb")
@PY.ULTRA
async def _(client, message):
    _msg = f"<b>Processing...</b>"
    msg = await message.reply(_msg)
    try:
        if len(message.command) > 1:
            input_identifier = message.command[1]
        else:
            input_identifier = message.chat.id
    
        chat_id = await extract_id(message, input_identifier)
        bl = await DB.get_list_vars(client.me.id, "bcdb_users")

        if chat_id in bl:
            txt = f"<b>Is on the data broadcast!</b>"
        else:
            await DB.add_list_vars(client.me.id, "bcdb_users", chat_id)
            chat = await client.get_chat(chat_id)
            if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                txt = f"<b><a href=https://t.me/{chat.username or chat.id}>{chat.title}</a> has been added to the data broadcast!</b>"
            elif chat.type == ChatType.PRIVATE:
                user = await client.get_users(chat_id)
                user_full_name = f"[{user.first_name} {user.last_name or ''}](tg://user?id={user.id})"
                txt = f"<b>{user_full_name} has been added to the data broadcast!</b>"
            else:
                txt = f"<b>Chat ID {chat_id} has been added to the data broadcast!</b>"

        return await msg.edit(txt)
    except Exception as error:
        return await msg.edit(str(error))


@PY.UBOT("unbcdb")
@PY.ULTRA
async def _(client, message):
    _msg = f"<b>Processing...</b>"
    msg = await message.reply(_msg)
    try:
        if len(message.command) > 1:
            input_identifier = message.command[1]
        else:
            input_identifier = message.chat.id
    
        chat_id = await extract_id(message, input_identifier)
        blacklist = await DB.get_list_vars(client.me.id, "bcdb_users")

        if chat_id not in blacklist:
            response = f"<b>Not on the data broadcast!</b>"
        else:
            await DB.remove_list_vars(client.me.id, "bcdb_users", chat_id)
            chat = await client.get_chat(chat_id)
            if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                response = f"<b><a href=https://t.me/{chat.username or chat.id}>{chat.title}</a> has been removed from the blacklist broadcast!</b>"
            elif chat.type == ChatType.PRIVATE:
                user = await client.get_users(chat_id)
                user_full_name = f"[{user.first_name} {user.last_name or ''}](tg://user?id={user.id})"
                response = f"<b>{user_full_name} has been removed from the data broadcast!</b>"
            else:
                response = f"<b>Chat ID {chat_id} has been removed from the data broadcast!</b>"

        return await msg.edit(response)
    except Exception as error:
        return await msg.edit(str(error))

@PY.UBOT("delallbcdb")
@PY.ULTRA
async def _(client, message):
    msg = await message.reply("<b>Processing...</b>")
    
    try:
        await DB.remove_vars(client.me.id, f"bcdb_users")
        return await msg.edit("<b>All broadcast db removed successfully!</b>")
    except Exception as e:
        return await msg.edit(f"<b>Error:</b> {str(e)}")


@PY.UBOT("listbcdb")
@PY.ULTRA
async def _(client, message):
    _msg = "<b>Processing...</b>"
    mzg = await message.reply(_msg)

    bcdb = await DB.get_list_vars(client.me.id, "bcdb_users")
    total_bcdb = len(bcdb)

    list_text = "<b>List Data Broadcast!</b>\n\n"

    for chat_id in bcdb:
        try:
            chat = await client.get_chat(chat_id)
            if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                list_text += f'<a href="https://t.me/{chat.username or chat.id}">{chat.title}</a>\n'
            elif chat.type == ChatType.PRIVATE:
                user = await client.get_users(chat_id)
                user_full_name = f"{user.first_name or 'Unknown'} {user.last_name or ''}"
                list_text += f'<a href="tg://user?id={chat_id}">{user_full_name}</a>\n'
        except Exception:
            list_text += f"{chat_id}\n"

    list_text += f"<b>\nTotal Data Broadcast:</b> {total_bcdb}"
    return await mzg.edit(list_text)


@PY.UBOT("addbl|blbc")
async def _(client, message):
    _msg = f"<b>Processing...</b>"
    msg = await message.reply(_msg)
    try:
        if len(message.command) > 1:
            input_identifier = message.command[1]
        else:
            input_identifier = message.chat.id
    
        chat_id = await extract_id(message, input_identifier)
        bl = await DB.get_list_vars(client.me.id, "blacklist")

        if chat_id in bl:
            txt = f"<b>Is on the blacklist!</b>"
        else:
            await DB.add_list_vars(client.me.id, "blacklist", chat_id)
            chat = await client.get_chat(chat_id)
            if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                txt = f"<b><a href=https://t.me/{chat.username or chat.id}>{chat.title}</a> has been added to the blacklist broadcast!</b>"
            elif chat.type == ChatType.PRIVATE:
                user = await client.get_users(chat_id)
                user_full_name = f"[{user.first_name} {user.last_name or ''}](tg://user?id={user.id})"
                txt = f"<b>{user_full_name} has been added to the blacklist broadcast!</b>"
            else:
                txt = f"<b>Chat ID {chat_id} has been added to the blacklist broadcast!</b>"

        return await msg.edit(txt)
    except Exception as error:
        return await msg.edit(str(error))


@PY.UBOT("delallbl")
async def _(client, message):
    msg = await message.reply("<b>Processing...</b>")
    
    try:
        await DB.remove_vars(client.me.id, f"blacklist")
        return await msg.edit("<b>All blacklist removed successfully!</b>")
    except Exception as e:
        return await msg.edit(f"<b>Error:</b> {str(e)}")


@PY.UBOT("unbl")
async def _(client, message):
    _msg = f"<b>Processing...</b>"
    msg = await message.reply(_msg)
    try:
        if len(message.command) > 1:
            input_identifier = message.command[1]
        else:
            input_identifier = message.chat.id
    
        chat_id = await extract_id(message, input_identifier)
        blacklist = await DB.get_list_vars(client.me.id, "blacklist")

        if chat_id not in blacklist:
            response = f"<b>Not on the blacklist!</b>"
        else:
            await DB.remove_list_vars(client.me.id, "blacklist", chat_id)
            chat = await client.get_chat(chat_id)
            if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                response = f"<b><a href=https://t.me/{chat.username or chat.id}>{chat.title}</a> has been removed from the blacklist broadcast!</b>"
            elif chat.type == ChatType.PRIVATE:
                user = await client.get_users(chat_id)
                user_full_name = f"[{user.first_name} {user.last_name or ''}](tg://user?id={user.id})"
                response = f"<b>{user_full_name} has been removed from the blacklist broadcast!</b>"
            else:
                response = f"<b>Chat ID {chat_id} has been removed from the blacklist broadcast!</b>"

        return await msg.edit(response)
    except Exception as error:
        return await msg.edit(str(error))


@PY.UBOT("listbl")
async def _(client, message):
    _msg = "<b>Processing...</b>"
    mzg = await message.reply(_msg)

    blacklist = await DB.get_list_vars(client.me.id, "blacklist")
    total_blacklist = len(blacklist)

    list_text = "<b>Daftar Blacklist Broadcast!</b>\n\n"

    for chat_id in blacklist:
        try:
            chat = await client.get_chat(chat_id)
            if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                list_text += f'<a href="https://t.me/{chat.username or chat.id}">{chat.title}</a>\n'
            elif chat.type == ChatType.PRIVATE:
                user = await client.get_users(chat_id)
                user_full_name = f"{user.first_name or 'Unknown'} {user.last_name or ''}"
                list_text += f'<a href="tg://user?id={chat_id}">{user_full_name}</a>\n'
        except Exception:
            list_text += f"{chat_id}\n"

    list_text += f"<b>\nTotal Blacklist Broadcast:</b> {total_blacklist}"
    return await mzg.edit(list_text)


AG = []
LT = []


@PY.UBOT("autogcast")
async def _(client, message):
    msg = await message.reply(f"<b>Processing...</b>")
    type, value = type_and_text(message)
    auto_text_vars = await DB.get_vars(client.me.id, "auto_gcast_text")

    if type == "on":
        if not auto_text_vars:
            return await msg.edit(
                "<b>Please set the text first!</b>"
            )

        if client.me.id not in AG:
            await msg.edit("<b>Auto gcast is activated!</b>")

            AG.append(client.me.id)

            done = 0
            while client.me.id in AG:
                delay = await DB.get_vars(client.me.id, "auto_gcast_delay") or 1
                blacklist = await DB.get_list_vars(client.me.id, "blacklist")
                txt = random.choice(auto_text_vars)

                group = 0
                async for dialog in client.get_dialogs():
                    if (
                        dialog.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP)
                        and dialog.chat.id not in blacklist
                    ):
                        try:
                            await asyncio.sleep(1)
                            await client.send_message(dialog.chat.id, f"{txt} {random.choice(range(999))}")
                            group += 1
                        except FloodWait as e:
                            await asyncio.sleep(e.value)
                            await client.send_message(dialog.chat.id, f"{txt} {random.choice(range(999))}")
                            group += 1
                        except Exception:
                            pass

                if client.me.id not in AG:
                    return

                done += 1
                await msg.reply(f"""
<b>Auto_gcast sent!</b>
<b>Round:</b> {done}
<b>Succes:</b> {group}
<b>Waiting:</b> {delay} <b>Minute</b>
""",
                    quote=True,
                )
                await asyncio.sleep(int(60 * int(delay)))
        else:
            return await msg.delete()

    elif type == "off":
        if client.me.id in AG:
            AG.remove(client.me.id)
            return await msg.edit("<b>Auto gcast is disabled!</b>")
        else:
            return await msg.delete()

    elif type == "text":
        if not value:
            return await msg.edit(
                f"<b>Please enter the text to be set!</b>"
            )
        await add_auto_text(client, value)
        return await msg.edit("<b>Text has been successfully set!</b>")

    elif type == "delay":
        if not int(value):
            return await msg.edit(
                f"<b>Enter the number of round delays!</b>"
            )
        await DB.set_vars(client.me.id, "auto_gcast_delay", value)
        return await msg.edit(
            f"<b>Successfully set to {value} minute!</b>"
        )

    elif type == "remove":
        if not value:
            return await msg.edit(
                f"<b>Enter the number in the text list to be deleted!</b>"
            )
        if value == "all":
            await DB.set_vars(client.me.id, "auto_gcast_text", [])
            return await msg.edit("<b>All gcast auto text lists have been deleted!</b>")
        try:
            value = int(value) - 1
            auto_text_vars.pop(value)
            await DB.set_vars(client.me.id, "auto_gcast_text", auto_text_vars)
            return await msg.edit(
                f"<b>The {value+1} text list has been successfully deleted!</b>"
            )
        except Exception as error:
            return await msg.edit(str(error))

    elif type == "list":
        if not auto_text_vars:
            return await msg.edit("<b>Auto gcast text empty!</b>")
        txt = "<b>List auto gacst text!</b>\n\n"
        for num, x in enumerate(auto_text_vars, 1):
            txt += f"<b>{num}. </b>{x}\n\n"
        txt += f"<b>\nFor deleted text:\n<code>{message.text.split()[0]} remove</code> number list</b>"
        return await msg.edit(txt)

    elif type == "limit":
        if value == "off":
            if client.me.id in LT:
                LT.remove(client.me.id)
                return await msg.edit("<b>Auto cek limit disabled!</b>")
            else:
                return await msg.delete()

        elif value == "on":
            if client.me.id not in LT:
                LT.append(client.me.id)
                await msg.edit("<b>Auto cek limit started!</b>")
                while client.me.id in LT:
                    for x in range(2):
                        await limit_cmd(client, message)
                        await asyncio.sleep(5)
                    await asyncio.sleep(1200)
            else:
                return await msg.delete()
        else:
             return await msg.edit(f"<b>Use on off to enable or disable!</b>")

    else:
        return await msg.edit(f"<b>Please set auto gcast to the correct format!</b>")


async def add_auto_text(client, text):
    auto_text = await DB.get_vars(client.me.id, "auto_gcast_text") or []
    auto_text.append(text)
    await DB.set_vars(client.me.id, "auto_gcast_text", auto_text)
