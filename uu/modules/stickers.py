import asyncio
import os

from pyrogram import emoji
from pyrogram.errors import StickersetInvalid, YouBlockedUser
from pyrogram.raw.functions.messages import DeleteHistory, GetStickerSet
from pyrogram.raw.types import InputStickerSetShortName

from uu import *


__MODULE__ = "Stickers"
__HELP__ = """
<b>Menu Stickers!</b>

<b>Create quote!</b>
 <code>{0}q</code>

<b>Added text to stickers or img</b>
 <code>{0}mmf</code>

<b>Added or creat new stickers!</b>
 <code>{0}kang</code>
"""


@PY.UBOT("q")
async def _(client, message):
    info = await message.reply("<b>Processing...</b>", quote=True)
    await client.unblock_user("@QuotLyBot")
    if message.reply_to_message:
        if len(message.command) < 2:
            msg = [message.reply_to_message]
        else:
            try:
                count = int(message.command[1])
            except ValueError as error:
                return await info.edit(str(error))
            msg = [
                i
                for i in await client.get_messages(
                    chat_id=message.chat.id,
                    message_ids=range(message.reply_to_message.id, message.reply_to_message.id + count),
                    replies=-1,
                )
            ]
        try:
            for x in msg:
                await x.forward("@QuotLyBot")
        except Exception:
            pass
        await asyncio.sleep(9)
        await info.delete()
        async for quotly in client.get_chat_history("@QuotLyBot", limit=1):
            if not quotly.sticker:
                await message.reply(f"<b>Unable to respond</b>", quote=True)
            else:
                sticker = await client.download_media(quotly)
                await message.reply_sticker(sticker, quote=True)
                os.remove(sticker)
    else:
        if len(message.command) < 2:
            return await info.edit("<b>Reply to text or media!</b>")
        else:
            msg = await client.send_message("@QuotLyBot", f"/qcolor {message.command[1]}")
            await asyncio.sleep(1)
            get = await client.get_messages("@QuotLyBot", msg.id + 1)
            await info.edit(f"<b>color is set to:</b> {get.text.split(':')[1]}")
    user_info = await client.resolve_peer("@QuotLyBot")
    return await client.invoke(DeleteHistory(peer=user_info, max_id=0, revoke=True))


@PY.UBOT("mmf")
async def _(client, message):
    if not message.reply_to_message or not message.reply_to_message.media:
        return await message.reply("<b>Reply to stickers or img!</b>")

    reply_message = message.reply_to_message
    file = await client.download_media(reply_message)
    if not file:
        return await message.reply("<b>Failed to download media!</b>")

    text = get_arg(message)
    if not any(char.isalpha() for char in text):
        os.remove(file)
        return await message.reply("<b>Please provide text with alphabets!</b>")
    
    has_uppercase = any(char.isupper() for char in text)
    has_lowercase = any(char.islower() for char in text)

    if not has_uppercase and not has_lowercase:
        os.remove(file)
        return await message.reply("<b>Please provide text with both uppercase and lowercase letters!</b>")

    Tm = await message.reply("<b>Processing...</b>")
    try:
        meme = await add_text_img(file, text)
        await asyncio.gather(
            Tm.delete(),
            client.send_sticker(
                message.chat.id,
                sticker=meme,
                reply_to_message_id=message.id,
            ),
        )
        os.remove(meme)
    except Exception as e:
        await Tm.edit(f"<b>Error: {e}</b>")
    finally:
        os.remove(file)
    

@PY.UBOT("kang")
async def _(client, message):
    replied = message.reply_to_message
    msg_text = await message.reply(f"<b>Processing...</b>")
    media_ = None
    emoji_ = None
    is_anim = False
    is_video = False
    resize = False
    ff_vid = False
    if replied and replied.media:
        if replied.photo:
            resize = True
        elif replied.document and "image" in replied.document.mime_type:
            resize = True
            replied.document.file_name
        elif replied.document and "tgsticker" in replied.document.mime_type:
            is_anim = True
            replied.document.file_name
        elif replied.document and "video" in replied.document.mime_type:
            resize = True
            is_video = True
            ff_vid = True
        elif replied.animation:
            resize = True
            is_video = True
            ff_vid = True
        elif replied.video:
            resize = True
            is_video = True
            ff_vid = True
        elif replied.sticker:
            if not replied.sticker.file_name:
                await msg_text.edit("<b>Sticker doesn't have a name!</b>")
                return
            emoji_ = replied.sticker.emoji
            is_anim = replied.sticker.is_animated
            is_video = replied.sticker.is_video
            if not (replied.sticker.file_name.endswith(".tgs") or replied.sticker.file_name.endswith(".webm")):
                resize = True
                ff_vid = True
        else:
            await msg_text.edit("<b>File invalid</b>")
            return
        media_ = await client.download_media(replied)
    else:
        await msg_text.edit("<b>Reply to media photo,gif,sticker!</b>")
        return
    if media_:
        args = get_arg(message)
        pack = 1
        if len(args) == 2:
            emoji_, pack = args
        elif len(args) == 1:
            if args[0].isnumeric():
                pack = int(args[0])
            else:
                emoji_ = args[0]

        if emoji_ and emoji_ not in (getattr(emoji, _) for _ in dir(emoji) if not _.startswith("_")):
            emoji_ = None
        if not emoji_:
            emoji_ = "✨"

        u_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}"
        packname = f"stkr_{str(message.from_user.id)}_by_{TB.me.username}"
        custom_packnick = f"{u_name} sticker pack"
        packnick = f"{custom_packnick} vol.{pack}"
        cmd = "/newpack"
        if resize:
            try:
                media_ = await resize_media(media_, is_video, ff_vid)
            except Exception as error:
                return await msg_text.edit(str(error))
        if is_anim:
            packname += "_animated"
            packnick += " (animated)"
            cmd = "/newanimated"
        if is_video:
            packname += "_video"
            packnick += " (video)"
            cmd = "/newvideo"
        exist = False
        while True:
            try:
                exist = await client.invoke(GetStickerSet(stickerset=InputStickerSetShortName(short_name=packname), hash=0))
            except StickersetInvalid:
                exist = False
                break
            limit = 50 if (is_video or is_anim) else 120
            if exist.set.count >= limit:
                pack += 1
                packname = f"stkr_{str(message.from_user.id)}_by_{TB.me.username}"
                packnick = f"{custom_packnick} vol.{pack}"
                if is_anim:
                    packname += f"_anim{pack}"
                    packnick += f" (animated){pack}"
                if is_video:
                    packname += f"_video{pack}"
                    packnick += f" (video){pack}"
                await msg_text.edit(f"<b>Created new sticker pac {pack} because the pack is full!</b>")
                continue
            break
        if exist is not False:
            try:
                await client.send_message("stickers", "/addsticker")
            except YouBlockedUser:
                await client.unblock_user("stickers")
                await client.send_message("stickers", "/addsticker")
            except Exception as e:
                return await msg_text.edit(f"<b>ERROR:</b> <code>{e}</code>")
            await asyncio.sleep(2)
            await client.send_message("stickers", packname)
            await asyncio.sleep(2)
            limit = "50" if is_anim else "120"
            while limit in await get_response(message, client):
                await DB.get_vars(client.me.id, "kang_pack") or "5280786999102415056"
                pack += 1
                packname = f"stkr_{str(message.from_user.id)}_by_{TB.me.username}"
                packnick = f"{custom_packnick} vol.{pack}"
                if is_anim:
                    packname += "_anim"
                    packnick += " (animated)"
                if is_video:
                    packname += "_video"
                    packnick += " (video)"
                await msg_text.edit(f"<b>Created new sticker pac {pack} because the pack is full!</b>")
                await client.send_message("stickers", packname)
                await asyncio.sleep(2)
                if await get_response(message, client) == "Invalid pack selected.":
                    await client.send_message("stickers", cmd)
                    await asyncio.sleep(2)
                    await client.send_message("stickers", packnick)
                    await asyncio.sleep(2)
                    await client.send_document("stickers", media_)
                    await asyncio.sleep(2)
                    await client.send_message("Stickers", emoji_)
                    await asyncio.sleep(2)
                    await client.send_message("Stickers", "/publish")
                    await asyncio.sleep(2)
                    if is_anim:
                        await client.send_message(
                            "Stickers",
                            f"<code>{packnick}</code>",
                        )
                        await asyncio.sleep(2)
                    await client.send_message("Stickers", "/skip")
                    await asyncio.sleep(2)
                    await client.send_message("Stickers", packname)
                    await asyncio.sleep(2)
                    await msg_text.edit(f"<b>Sticker Succes Added! [klick here](https://t.me/addstickers/{packname})</b>")
                    await asyncio.sleep(2)
                    user_info = await client.resolve_peer("@Stickers")
                    return await client.invoke(DeleteHistory(peer=user_info, max_id=0, revoke=True))
            await client.send_document("stickers", media_)
            await asyncio.sleep(2)
            if await get_response(message, client) == "Sorry, the file type is invalid.":
                await msg_text.edit("<b>Failed added stickers!</b>")
                return
            await client.send_message("Stickers", emoji_)
            await asyncio.sleep(2)
            await client.send_message("Stickers", "/done")
        else:
            await msg_text.edit("<b>Created new stickers pack</b>")
            try:
                await client.send_message("Stickers", cmd)
            except YouBlockedUser:
                await client.unblock_user("stickers")
                await client.send_message("stickers", "/addsticker")
            await asyncio.sleep(2)
            await client.send_message("Stickers", packnick)
            await asyncio.sleep(2)
            await client.send_document("stickers", media_)
            await asyncio.sleep(2)
            if await get_response(message, client) == "Sorry, the file type is invalid.":
                await msg_text.edit("<b>Failded added stickers!</b>")
                return
            await client.send_message("Stickers", emoji_)
            await asyncio.sleep(2)
            await client.send_message("Stickers", "/publish")
            await asyncio.sleep(2)
            if is_anim:
                await client.send_message("Stickers", f"<code>{packnick}</code>")
                await asyncio.sleep(2)
            await client.send_message("Stickers", "/skip")
            await asyncio.sleep(2)
            await client.send_message("Stickers", packname)
            await asyncio.sleep(2)
        await msg_text.edit(f"<b>Sticker Succes Added! [klick here](https://t.me/addstickers/{packname})</b>")
        await asyncio.sleep(2)
        if os.path.exists(str(media_)):
            os.remove(media_)
        user_info = await client.resolve_peer("@Stickers")
        return await client.invoke(DeleteHistory(peer=user_info, max_id=0, revoke=True))


async def get_response(message, client):
    return [x async for x in client.get_chat_history("Stickers", limit=1)][0].text
