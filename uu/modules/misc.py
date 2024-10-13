import os
import asyncio
import random
import requests

from gc import get_objects
from uu.core.helpers.tools_fonts import *
from os import remove
from asyncio import sleep, gather

from pyrogram.types import *
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.raw.functions.messages import DeleteHistory
from telegraph import Telegraph, exceptions, upload_file
from pyrogram.enums import ChatType

from uu import *

from bs4 import BeautifulSoup
from io import BytesIO


__MODULE__ = "Misc"
__HELP__ = """
<b>Menu Misc!</b>

<b>Getting ids!</b>
 <code>{0}id</code>

<b>Get information users!</b>
 <code>{0}info</code>

<b>Uploading text or media to Telegraph!</b>
 <code>{0}tg</code>

<b>Create a carbonara text image!</b>
 <code>{0}carbon</code>

<b>Get timed media</b>
 <code>{0}colong</code>

<b>Get telegram content!</b>
 <code>{0}copy</code>

<b>Get history name user!</b>
 <code>{0}sg</code>

<b>Get font text!</b>
 <code>{0}font</code>

"""



async def send_function(client, chat_id, file_path, media_type, caption):
    if media_type == "photo":
        await client.send_photo(chat_id, file_path, caption=caption)
    elif media_type == "video":
        await client.send_video(chat_id, file_path, caption=caption)
    elif media_type == "audio":
        await client.send_audio(chat_id, file_path, caption=caption)
    elif media_type == "voice":
        await client.send_voice(chat_id, file_path, caption=caption)
    elif media_type == "document":
        await client.send_document(chat_id, file_path, caption=caption)

async def process_media(client, message, media_type, file):
    file_path = await client.download_media(file)
    caption = file.caption if hasattr(file, "caption") else ""
    await send_function(client, client.me.id, file_path, media_type, caption)
    os.remove(file_path)

@PY.UBOT("colong")
async def _(client, message):
    dia = message.reply_to_message
    if not dia:
        return await message.reply("<b>Reply to media message</b>")
    
    Tm = await message.reply("<b>Processing...</b>")
    media_types = ["photo", "video", "audio", "voice", "document"]

    for media_type in media_types:
        media = getattr(dia, media_type, None)
        if media:
            if media.file_size > 10_000_000:
                return await Tm.edit("File di atas 10MB tidak diizinkan")
            await process_media(client, message, media_type, media)
            await message.delete()
            return await Tm.delete()

    return await Tm.edit("<b>It seems like an error occurred!</b>")


async def make_carbon(code):
    url = "https://carbonara.solopov.dev/api/cook"
    async with aiosession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image


@PY.UBOT("carbon")
async def _(client, message):
    text = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption
    if not text:
        return await message.delete()
    ex = await message.reply("<b>Processing...</b>")
    carbon = await make_carbon(text)
    await ex.edit("<b>Uploading...</b>")
    await asyncio.gather(
        ex.delete(),
        client.send_photo(
            message.chat.id,
            carbon,
            caption=f"<b>Carbonised by :</b>{client.me.mention}",
        ),
    )
    carbon.close()


@PY.UBOT("copy")
async def _(client: Client, message):
    msg = message.reply_to_message or message
    Tm = await message.reply("<b>Processing...</b>")
    link = get_arg(message)
    
    if not link:
        await Tm.edit(f"<b>Provide the correct telegram content link?</b>")
        return
    
    if link.startswith(("https", "t.me")):
        msg_id = int(link.split("/")[-1])
        chat = int("-100" + str(link.split("/")[-2])) if "t.me/c/" in link else str(link.split("/")[-2])
        
        try:
            get = await client.get_messages(chat, msg_id)
            await get.copy(message.chat.id, reply_to_message_id=msg.id)
        except Exception as e:
            await client.send_message(
                message.chat.id,
                f"<b>Failed to get: {str(e)}</b>",
                reply_to_message_id=msg.id,
            )
        finally:
            await Tm.delete()
    else:
        await Tm.edit("<b>Enter the correct link!</b>")


@PY.UBOT("info")
async def _(client, message):
    user_id = await extract_user(message)
    Tm = await message.reply("</b>Processing...</b>")
    if not user_id:
        return await Tm.edit(
            "<b>Reply to user or username and user_id!</b>"
        )
    try:
        user = await client.get_users(user_id)
        username = f"@{user.username}" if user.username else "-"
        first_name = f"{user.first_name}" if user.first_name else "-"
        last_name = f"{user.last_name}" if user.last_name else "-"
        fullname = (
            f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
        )
        user_details = (await client.get_chat(user.id)).bio
        bio = f"{user_details}" if user_details else "-"
        h = f"{user.status}"
        if h.startswith("UserStatus"):
            y = h.replace("UserStatus.", "")
            status = y.capitalize()
        else:
            status = "-"
        dc_id = f"{user.dc_id}" if user.dc_id else "-"
        common = await client.get_common_chats(user.id)
        out_str = f"""
<b>User Information!</b>

 <b>Dc Id:</b> <code>{dc_id}</code>
 <b>User Id:</b> <code>{user.id}</code>
 <b>first Name:</b> {first_name}
 <b>Last Name:</b> {last_name}
 <b>Username:</b> {username}
 <b>Premium:</b> <code>{user.is_premium}</code>

 <b>User permanent link:</b> <a href=tg://user?id={user.id}>{fullname}</a>
"""
        
        await Tm.edit(out_str, disable_web_page_preview=True)
    except Exception as e:
        return await Tm.edit(f"ɪɴꜰᴏ: {e}")



@PY.UBOT("id")
async def _(client, message):
    text = f"<b>Message Id:</b> {message.id}\n"

    if message.chat.type == ChatType.CHANNEL:
        text += f"<b>Chat id:</b> {message.sender_chat.id}\n"
    else:
        text += f"<b>Your id:</b> {message.from_user.id}\n\n"

        if len(message.command) > 1:
            try:
                user = await client.get_chat(message.text.split()[1])
                text += f"<b>User id:</b> {user.id}\n\n"
            except:
                return await message.reply("<b>User not found!</b>")

        text += f"<b>Chat id:</b> {message.chat.id}\n\n"

    if message.reply_to_message:
        id_ = (
            message.reply_to_message.from_user.id
            if message.reply_to_message.from_user
            else message.reply_to_message.sender_chat.id
        )
        file_info = get_file_id(message.reply_to_message)
        if file_info:
            text += f"<b>ᴍᴇᴅɪᴀ ɪᴅ:</b> {file_info.file_id}\n\n"
        text += (
            f"<b>Replied message id:</b> {message.reply_to_message.id}\n"
            f"<b>Replied user id:</b> {id_}"
        )

    return await message.reply(text, disable_web_page_preview=True)


@PY.UBOT("tg")
async def _(client, message):
    XD = await message.reply("<b>Processing</b>")
    if not message.reply_to_message:
        return await XD.edit(
            "<b>Reply to messages or media!</b>"
        )
    telegraph = Telegraph()
    if message.reply_to_message.media:
        m_d = await dl_pic(client, message.reply_to_message)
        try:
            media_url = upload_file(m_d)
        except exceptions.TelegraphException as exc:
            return await XD.edit(f"<code>{exc}</code>")
        U_done = f"<b>Successfully uploaded to</b> <a href='https://telegra.ph/{media_url[0]}'>telegraph</a>"
        await XD.edit(U_done)
    elif message.reply_to_message.text:
        page_title = f"{client.me.first_name} {client.me.last_name or ''}"
        page_text = message.reply_to_message.text
        page_text = page_text.replace("\n", "<br>")
        try:
            response = telegraph.create_page(page_title, html_content=page_text)
        except exceptions.TelegraphException as exc:
            return await XD.edit(f"<code>{exc}</code>")
        wow_graph = f"<b>Successfully uploaded to</b> <a href='https://telegra.ph/{response['path']}'>telegraph</a>"
        await XD.edit(wow_graph)


@PY.UBOT("sg")
async def _(client, message):
    get_user = await extract_user(message)
    lol = await message.reply("<b>Processing...</b>")
    if not get_user:
        return await lol.edit("<b>User not found!</b>")
    try:
        user_id = (await client.get_users(get_user)).id
    except Exception:
        try:
            user_id = int(message.command[1])
        except Exception as error:
            return await lol.edit(error)
    bot = ["@Sangmata_bot", "@SangMata_beta_bot"]
    getbot = random.choice(bot)
    await client.unblock_user(getbot)
    txt = await client.send_message(getbot, user_id)
    await asyncio.sleep(4)
    await txt.delete()
    await lol.delete()
    async for name in client.search_messages(getbot, limit=2):
        if not name.text:
            await message.reply(
                f"{getbot} <b>Unable to respond!</b>", quote=True
            )
        else:
            await message.reply(name.text, quote=True)
    user_info = await client.resolve_peer(getbot)
    return await client.invoke(DeleteHistory(peer=user_info, max_id=0, revoke=True))


@PY.UBOT("font")
async def _(client, message):
    if message.reply_to_message:
        if message.reply_to_message.text:
            query = id(message)
        else:
            return await message.reply("<b>Harap reply text</b>")
    else:
        if len(message.command) < 2:
            return await message.reply(f"<b><code>{message.text}</code> [Reply/Text]</b>")
        else:
            query = id(message)
    try:
        x = await client.get_inline_bot_results(TB.me.username, f"get_font {query}")
        return await message.reply_inline_bot_result(x.query_id, x.results[0].id)
    except Exception as error:
        return await message.reply(error)


@PY.INLINE("^get_font")
async def _(client, inline_query):
    get_id = int(inline_query.query.split(None, 1)[1])
    buttons = InlineKeyboard(row_width=3)
    keyboard = []
    for X in query_fonts[0]:
        keyboard.append(
            InlineKeyboardButton(X, callback_data=f"get {get_id} {query_fonts[0][X]}")
        )
    buttons.add(*keyboard)
    buttons.row(InlineKeyboardButton("►", callback_data=f"next {get_id}"))
    await client.answer_inline_query(
        inline_query.id,
        cache_time=0,
        results=[
            (
                InlineQueryResultArticle(
                    title="get font!",
                    reply_markup=buttons,
                    input_message_content=InputTextMessageContent(
                        "<b>Silahkan pilih font!</b>"
                    ),
                )
            )
        ],
    )


@PY.CALLBACK("^get")
async def _(client, callback_query):
    try:
        q = int(callback_query.data.split()[1])
        m = [obj for obj in get_objects() if id(obj) == q][0]
        new = str(callback_query.data.split()[2])
        if m.reply_to_message:
            text = m.reply_to_message.text
        else:
            text = m.text.split(None, 1)[1]
        get_new_font = gens_font(new, text)
        return await callback_query.edit_message_text(get_new_font)
    except Exception as error:
        return await callback_query.answer(f"Error: {error}", True)


@PY.CALLBACK("^next")
async def _(client, callback_query):
    try:
        get_id = int(callback_query.data.split()[1])
        buttons = InlineKeyboard(row_width=3)
        keyboard = []
        for X in query_fonts[1]:
            keyboard.append(
                InlineKeyboardButton(
                    X, callback_data=f"get {get_id} {query_fonts[1][X]}"
                )
            )
        buttons.add(*keyboard)
        buttons.row(InlineKeyboardButton("◄", callback_data=f"prev {get_id}"))
        return await callback_query.edit_message_reply_markup(reply_markup=buttons)
    except Exception as error:
        return await callback_query.answer(f"Error: {error}", True)


@PY.CALLBACK("^prev")
async def _(client, callback_query):
    try:
        get_id = int(callback_query.data.split()[1])
        buttons = InlineKeyboard(row_width=3)
        keyboard = []
        for X in query_fonts[0]:
            keyboard.append(
                InlineKeyboardButton(
                    X, callback_data=f"get {get_id} {query_fonts[0][X]}"
                )
            )
        buttons.add(*keyboard)
        buttons.row(InlineKeyboardButton("►", callback_data=f"next {get_id}"))
        return await callback_query.edit_message_reply_markup(reply_markup=buttons)
    except Exception as error:
        return await callback_query.answer(f"❌ Error: {error}", True)
