import asyncio
import io
import os

import requests
from config import Config
from pyrogram import raw

from uu import *

__MODULE__ = "Image"
__HELP__ = """
<b>Menu Image!</b>

<b>Get photo anime!</b>
 <code>{0}wall</code> or {0}waifu</code>

<b>Deleting background</b>(ultra)
 <code>{0}rbg</code>

<b>Get gif</b>
 <code>{0}gif [judul]</code>

<b>Get photo</b>(ultra)
 <code>{0}pic [judul]</code>
"""



@PY.UBOT("rbg")
@PY.ULTRA
async def _(client, message):
    if Config.RMBG_API is None:
        return
    if message.reply_to_message:
        reply_message = message.reply_to_message
        xx = await message.reply("<b>Processing...</b>")
        try:
            if (
                isinstance(reply_message.media, raw.types.MessageMediaPhoto)
                or reply_message.media
            ):
                downloaded_file_name = await client.download_media(
                    reply_message, "./downloads/"
                )
                await xx.edit("<b>Erase background...</b>")
                output_file_name = await ReTrieveFile(downloaded_file_name)
                os.remove(downloaded_file_name)
            else:
                await xx.edit("<b>Erase invalid!</b>")
        except Exception as e:
            await xx.edit(f"{(str(e))}")
            return
        contentType = output_file_name.headers.get("content-type")
        if "image" in contentType:
            with io.BytesIO(output_file_name.content) as remove_bg_image:
                remove_bg_image.name = "rbg.png"
                await client.send_document(
                    message.chat.id,
                    document=remove_bg_image,
                    force_document=True,
                    reply_to_message_id=message.id,
                )
                await xx.delete()
        else:
            await xx.edit(
                "<b>Invalid api key!".format(
                    output_file_name.content.decode("UTF-8")
                ),
            )
    else:
        return await message.reply("<b>Reply to the picture!</b>")


@PY.UBOT("wall|waifu")
async def _(client, message):
    msg = await message.reply("<b>Processing...</b>", quote=True)
    if message.command[0] == "wall":
        photo = await API.wall(client)
        try:
            await photo.copy(message.chat.id, reply_to_message_id=message.id)
            return await msg.delete()
        except Exception as error:
            return await msg.edit(error)
    elif message.command[0] == "waifu":
        photo = API.waifu()
        try:
            await message.reply_photo(photo, quote=True)
            return await msg.delete()
        except Exception as error:
            return await msg.edit(error)


@PY.UBOT("pic")
async def pic_bing_cmd(client, message):
    TM = await message.reply(f"Processing...")
    await asyncio.sleep(2)
    if len(message.command) < 2:
        return await TM.edit(f" <code>{message.text}</code> [query]")
    x = await client.get_inline_bot_results(
        message.command[0], message.text.split(None, 1)[1]
    )
    await TM.delete()
    get_media = []
    for X in range(5):
        try:
            saved = await client.send_inline_bot_result(
                client.me.id, x.query_id, x.results[random.randrange(30)].id
            )
            saved = await client.get_messages(
                client.me.id, int(saved.updates[1].message.id), replies=0
            )
            get_media.append(InputMediaPhoto(saved.photo.file_id))
        except BaseException:
            await TM.edit(f"<b>Image photo ke {X} tidak ditemukan!!</b>")
    await saved.delete()          
    await client.send_media_group(
        message.chat.id,
        get_media,
        reply_to_message_id=message.id,
    )


@PY.UBOT("gif")
async def gif_cmd(client, message):
    Tm = await message.reply(f"Processing...")
    await asyncio.sleep(2)
    if len(message.command) < 2:
        return await Tm.edit(f" <code>{message.text}</code> [query]")
    x = await client.get_inline_bot_results(
        message.command[0], message.text.split(None, 1)[1]
    )
    await Tm.delete()
    try:
        saved = await client.send_inline_bot_result(
            client.me.id, x.query_id, x.results[random.randrange(30)].id
        )
    except BaseException:
        await Tm.edit(f"<b>Gif tidak ditemukan!</b>")
    saved = await client.get_messages(
        client.me.id, int(saved.updates[1].message.id), replies=0
    )
    await saved.delete()
    await client.send_animation(
        message.chat.id, saved.animation.file_id, reply_to_message_id=message.id
    )