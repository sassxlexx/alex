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


__MODULE__ = "Music Tools"
__HELP__ = """
<b>Menu Music Tools!</b>


<b>Playing music in group calls!</b>(ultra)
 <code>{0}play [judul]</code>

<b>Playing video in group calls!</b>(ultra)
 <code>{0}vplay [judul]</code>

<b>End stream and music!</b>(ultra)
 <code>{0}end or {0}stop</code>
"""


@TU.pytgcall_close_stream()
async def _(client, update):
    chat_id = update.chat_id
    try:
        await client.leave_call(chat_id)
    except (NotInGroupCallError, NoActiveGroupCall):
        pass


@PY.UBOT("play")
@PY.ULTRA
@PY.GROUP
async def _(client, message):
    if message.reply_to_message:
        media = message.reply_to_message.audio or message.reply_to_message.voice
        if media:
            infomsg = await message.reply(f"<b>Downloading {'audio' if message.reply_to_message.audio else 'voice'}...</b>")
            file_name = await client.download_media(media)
            title = "Audio" if message.reply_to_message.audio else "Voice"
            duration = media.duration or 0
            channel = "Local Audio" if message.reply_to_message.audio else "Local Voice"
            views = "N/A"
            thumb = None
    else:
        if len(message.command) < 2:
            return await message.reply("<b>Provide the title of the song you want!</b>")

        infomsg = await message.reply("<b>Search...</b>")
        query = message.text.split(None, 1)[1]
        try:
            search_result = VideosSearch(query, limit=1).result()["result"][0]
            link = f"https://youtu.be/{search_result['id']}"
        except Exception:
            return await infomsg.edit("<b>Music search failed</b>")

        try:
            file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(link, as_video=False)
        except Exception:
            return await infomsg.edit("<b>Failed to play music!</b>")

    chat_id = message.chat.id
    a_calls = await client.call_py.calls
    if_chat = a_calls.get(chat_id)
    if if_chat:
        return await infomsg.edit("<b>Already play music in voice chat!</b>")

    try:
        await client.call_py.play(chat_id, MediaStream(
            file_name,
            video_flags=MediaStream.Flags.IGNORE,
            audio_parameters=AudioQuality.STUDIO,
        ))
        await infomsg.edit(f"""
<b>Playing song!</b>

<b>Title:</b> {title}
<b>Duration:</b> {timedelta(seconds=duration)}
<b>Views:</b> {views}
<b>Channel:</b> {channel}
""")
    except NoActiveGroupCall:
        await infomsg.edit("<b>No active voice calls!</b>")
    except Exception:
        await infomsg.edit("<b>Failed to play audio!</b>")
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)
        if thumb and os.path.exists(thumb):
            os.remove(thumb)


@PY.UBOT("vplay")
@PY.ULTRA
@PY.GROUP
async def _(client, message):
    if message.reply_to_message:
        media = message.reply_to_message.video
        if media:
            infomsg = await message.reply(f"<b>Downloading {'video' if message.reply_to_message.video else 'video'}...</b>")
            file_name = await client.download_media(media)
            title = "Video" if message.reply_to_message.video else "Video"
            duration = media.duration or 0
            channel = "Local Video" if message.reply_to_message.video else "Local Video"
            views = "N/A"
            thumb = None
    else:
        if len(message.command) < 2:
            return await message.reply("<b>Provide the title of the video you want!</b>")

        infomsg = await message.reply("<b>Search...</b>")
        query = message.text.split(None, 1)[1]
        try:
            search_result = VideosSearch(query, limit=1).result()["result"][0]
            link = f"https://youtu.be/{search_result['id']}"
        except Exception:
            return await infomsg.edit("<b>Video search failed</b>")

        try:
            file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(link, as_video=True)
        except Exception:
            return await infomsg.edit("<b>Failed to play video!</b>")

    chat_id = message.chat.id
    a_calls = await client.call_py.calls
    if_chat = a_calls.get(chat_id)
    if if_chat:
        return await infomsg.edit("<b>Already play video in call chat!</b>")

    try:
        await client.call_py.play(chat_id, MediaStream(file_name))
        await infomsg.edit(f"""
<b>Playing video!</b>

<b>Title:</b> {title}
<b>Duration:</b> {timedelta(seconds=duration)}
<b>Views:</b> {views}
<b>Channel:</b> {channel}
""")
    except NoActiveGroupCall:
        await infomsg.edit("<b>No active voice calls!</b>")
    except Exception:
        await infomsg.edit("<b>Failed to play video!</b>")
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)
        if thumb and os.path.exists(thumb):
            os.remove(thumb)


@PY.UBOT("end|stop")
@PY.ULTRA
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
        return await message.reply(f"<b>Ended successfully!</b>")
    except GroupCallNotFound:
        return await message.reply("<b>Not playing anything!</b>")
    except Exception as e:
        return await message.reply(f"<b>Error:</b> {e}")


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