import os
import subprocess
import sys
import traceback

from io import BytesIO, StringIO

from uu import *
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from pyrogram.types import *
from pytz import timezone

import asyncio

from pyrogram.enums import UserStatus
import random
from asyncio import sleep
from config import Config

from pyrogram import Client, enums, filters, raw
from pyrogram.types import Message

from config import Config


__MODULE__ = "devs"
__HELP__ = """
<b>Menu devs!</b>

<b>Adding users to e!</b>
 <code>{0}e</code>
"""

@TU.on_message(filters.group & filters.user(Config.OWNER_ID) & filters.command("tes"))
async def _(client, message):
    emoji = ["🔥", "👻", "❤️‍🔥", "🗿", "😈", "🍓", "🙊", "🍌", "💩", "🎃", "🏆", "⚡", "🍓"]
    random_emoji = random.choice(emoji)
    chat = message.chat.id
    id = message.id
    await sleep(1)
    await client.send_reaction(chat_id=chat, message_id=id, emoji=random_emoji)


async def send_large_output(message, output):
    with BytesIO(str.encode(str(output))) as out_file:
        out_file.name = "result.txt"
        await message.reply_document(document=out_file)


async def handle_clean(message):
    # Define paths to clean
    temp_dirs = ['/tmp', '/var/tmp', 'path_to_cache_directory']

    deleted_files = 0
    deleted_dirs = 0

    for temp_dir in temp_dirs:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                try:
                    os.remove(os.path.join(root, file))
                    deleted_files += 1
                except Exception as e:
                    pass
            for dir in dirs:
                try:
                    os.rmdir(os.path.join(root, dir))
                    deleted_dirs += 1
                except Exception as e:
                    pass

    await message.reply(f"<b>⥤ ʀᴇsᴜʟᴛ :</b><pre>✅ <b>ꜱʏꜱᴛᴇᴍ ʙᴇʀʜᴀsɪʟ ᴅɪ ʙᴇʀsɪʜᴋᴀɴ</b></pre>", quote=True)


async def handle_shutdown(message):
    await message.reply(f"<b>⥤ ʀᴇsᴜʟᴛ :</b><pre>✅ <b>ꜱʏꜱᴛᴇᴍ ʙᴇʀʜᴀꜱɪʟ ᴅɪ ᴍᴀᴛɪᴋᴀɴ</b></pre>", quote=True)
    os.system(f"kill -9 {os.getpid()}")


async def handle_restart(message):
    await message.reply(f"<b>⥤ ʀᴇsᴜʟᴛ :</b><pre>✅ <b>ꜱʏꜱᴛᴇᴍ ʙᴇʀʜᴀꜱɪʟ ᴅɪ ʀᴇꜱᴛᴀʀᴛ</b></pre>", quote=True)
    os.execl(sys.executable, sys.executable, "-m", "uu")


async def handle_update(message):
    out = subprocess.check_output(["git", "pull"]).decode("UTF-8")
    if "Already up to date." in str(out):
        return await message.reply(f"<b>⥤ ʀᴇsᴜʟᴛ :</b><pre>{out}</pre>", quote=True)
    elif int(len(str(out))) > 4096:
        await send_large_output(message, out)
    else:
        await message.reply(f"<b>⥤ ʀᴇsᴜʟᴛ :</b><pre>{out}</pre>", quote=True)
    os.execl(sys.executable, sys.executable, "-m", "uu")


async def process_command(message, command):
    result = (await bash(command))[0]
    if int(len(str(result))) > 4096:
        await send_large_output(message, result)
    else:
        await message.reply(f"<b>⥤ ʀᴇsᴜʟᴛ :</b><pre>{result}</pre>")


@PY.UBOT("sh")
@PY.OWNER
async def _(client, message):
    command = get_arg(message)
    msg = await message.reply("memproses...", quote=True)

    if not command:
        await msg.edit("noob")
        return
    try:
        if command == "shutdown":
            await msg.delete()
            await handle_shutdown(message)
        elif command == "restart":
            await msg.delete()
            await handle_restart(message)
        elif command == "update":
            await msg.delete()
            await handle_update(message)
        elif command == "clean":
            await msg.delete()
            await handle_clean(message)
        else:
            await process_command(message, command)
            await msg.delete()
    except Exception as error:
        await msg.edit(error)


@PY.UBOT("eval|e")
@PY.OWNER
async def _(client, message):
    if not get_arg(message):
        return
    TM = await message.reply_text("Processing ...")
    cmd = message.text.split(" ", maxsplit=1)[1]
    reply_to_ = message.reply_to_message or message
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "𝚂𝚄𝙲𝙲𝙴𝚂𝚂"
    final_output = "<b>⥤ ʀᴇsᴜʟᴛ :</b>\n"
    final_output += f"<pre language='python'>{evaluation.strip()}</pre>"
    if len(final_output) > 4096:
        with BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await reply_to_.reply_document(
                document=out_file,
                caption=cmd[: 4096 // 4 - 1],
                disable_notification=True,
                quote=True,
            )
    else:
        await reply_to_.reply_text(final_output, quote=True)
    await TM.delete()


@PY.UBOT("getubot")
async def _(client, message):
    uu = message.from_user.id
    if message.from_user.id == Config.OWNER_ID:
        pass
    else:
        return await message.reply("<b>You do not have access to use this command here</b>")
    try:
        x = await client.get_inline_bot_results(TB.me.username, "get_ubot")
        await message.reply_inline_bot_result(x.query_id, x.results[0].id)
    except Exception as error:
        await message.reply(error)


@PY.INLINE("^get_ubot")
async def get_ubot_inline(client, inline_query): 
    MSG_UBOT = await MSG.UBOT(0)
    results = [InlineQueryResultArticle(
        title="Help Menu!",
        reply_markup=InlineKeyboardMarkup(BTN.UBOT(TU._ubot[0].me.id, 0)),
        input_message_content=InputTextMessageContent(MSG_UBOT),
    )]

    await client.answer_inline_query(inline_query.id, cache_time=60, results=results)
