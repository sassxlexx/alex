import os
import wget
import asyncio
from datetime import timedelta
from time import time

from pyrogram import *


from uu import *


__MODULE__ = "Youtube"
__HELP__ = """
<b>Menu YouTube!</b>


<b>Download song from YouTube!</b>
 <code>{0}song</code>

<b>Download video from YouTube!</b>
 <code>{0}vsong</code>
"""



@PY.UBOT("vsong")
async def _(client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "<b>Video title not found!</b>",
        )
    infomsg = await message.reply_text("<b>ᴘᴇɴᴄᴀʀɪᴀɴ...</b>", quote=False)
    try:
        search = VideosSearch(message.text.split(None, 1)[1], limit=1).result()[
            "result"
        ][0]
        link = f"https://youtu.be/{search['id']}"
    except Exception as error:
        return await infomsg.edit(f"<b>Pencarian...\n\n{error}</b>")
    try:
        (
            file_name,
            title,
            url,
            duration,
            views,
            channel,
            thumb,
            data_ytp,
        ) = await YoutubeDownload(link, as_video=True)
    except Exception as error:
        return await infomsg.edit(f"<b>Downloader...\n\n{error}</b>")
    thumbnail = wget.download(thumb)
    await client.send_video(
        message.chat.id,
        video=file_name,
        thumb=thumbnail,
        file_name=title,
        duration=duration,
        supports_streaming=True,
        caption=data_ytp.format(
            "Video",
            title,
            timedelta(seconds=duration),
            views,
            channel,
            url,
            TB.me.mention,
        ),
        progress=progress,
        progress_args=(
            infomsg,
            time(),
            "<b>Downloader...</b>",
            f"{search['id']}.mp4",
        ),
        reply_to_message_id=message.id,
    )
    await infomsg.delete()
    for files in (thumbnail, file_name):
        if files and os.path.exists(files):
            os.remove(files)


@PY.UBOT("song")
async def _(client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "<b>Audio title not found!</b>",
        )
    infomsg = await message.reply_text("<b>Search...</b>", quote=False)
    try:
        search = VideosSearch(message.text.split(None, 1)[1], limit=1).result()[
            "result"
        ][0]
        link = f"https://youtu.be/{search['id']}"
    except Exception as error:
        return await infomsg.edit(f"<b>Search...\n\n{error}</b>")
    try:
        (
            file_name,
            title,
            url,
            duration,
            views,
            channel,
            thumb,
            data_ytp,
        ) = await YoutubeDownload(link, as_video=False)
    except Exception as error:
        return await infomsg.edit(f"<b>Downloader...\n\n{error}</b>")
    thumbnail = wget.download(thumb)
    await client.send_audio(
        message.chat.id,
        audio=file_name,
        thumb=thumbnail,
        file_name=title,
        performer=channel,
        duration=duration,
        caption=data_ytp.format(
            "Audio",
            title,
            timedelta(seconds=duration),
            views,
            channel,
            url,
            TB.me.mention,
        ),
        progress=progress,
        progress_args=(
            infomsg,
            time(),
            "<b>Downloader...</b>",
            f"{search['id']}.mp3",
        ),
        reply_to_message_id=message.id,
    )
    await infomsg.delete()
    for files in (thumbnail, file_name):
        if files and os.path.exists(files):
            os.remove(files)
