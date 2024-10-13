from pyrogram import Client, filters
from pyrogram.types import (InlineKeyboardMarkup, InlineQueryResultArticle,                            InputTextMessageContent, InlineKeyboardButton)
from datetime import datetime
import pytz

from uu import *

__MODULE__ = "Absen"
__HELP__ = """
<b>Menu Absen!</b>

<b>Absen List!</b>
 <code>{0}absen</code>

<b>Delete Absen!</b>
 <code>{0}delabsen</code>
"""

hadir_list = []

def get_hadir_list():
    return "\n".join([f"👤 {user['mention']} - {user['jam']}" for user in hadir_list])

@PY.UBOT("delabsen")
async def clear_absen_command(client, message):
    hadir_list.clear()
    await message.reply("Semua absen berhasil di hapus.")


@PY.INLINE("^absen_in")
async def absen_query(client, inline_query):
    user_id = inline_query.from_user.id
    mention = inline_query.from_user.mention
    timestamp = datetime.now(pytz.timezone('asia/Jakarta')).strftime("%d-%m-%Y")
    jam = datetime.now(pytz.timezone('asia/Jakarta')).strftime("%H:%M:%S")

    hadir_text = get_hadir_list()

    text = f"Absen tanggal:\n{timestamp}\n\nList absen:\n{hadir_text}\n\n"
    buttons = [[InlineKeyboardButton("Hadir", callback_data="absen_hadir")]]
    keyboard = InlineKeyboardMarkup(buttons)
    await client.answer_inline_query(
        inline_query.id,
        cache_time=0,
        results=[
            (
                InlineQueryResultArticle(
                    title="💬",
                    input_message_content=InputTextMessageContent(text),
                    reply_markup=keyboard
                )
            )
        ],
    )

@PY.CALLBACK("absen_hadir")
async def hadir_callback(client, callback_query):
    user_id = callback_query.from_user.id
    mention = callback_query.from_user.mention
    timestamp = datetime.now(pytz.timezone('asia/Jakarta')).strftime("%d-%m-%Y")
    jam = datetime.now(pytz.timezone('asia/Jakarta')).strftime("%H:%M:%S")
    if any(user['user_id'] == user_id for user in hadir_list):
        await callback_query.answer("Anda sudah melakukan absen.", show_alert=True)
    else:
        hadir_list.append({"user_id": user_id, "mention": mention, "jam": jam})
        hadir_text = get_hadir_list()
        text = f"Absen tanggal:\n{timestamp}\n\nList absen:\n{hadir_text}\n\n"
        buttons = [[InlineKeyboardButton("Hadir", callback_data="absen_hadir")]]
        keyboard = InlineKeyboardMarkup(buttons)
        await callback_query.edit_message_text(text, reply_markup=keyboard)

@PY.UBOT("absen")
async def absen_command(client, message):
    user_id = message.from_user.id
    mention = message.from_user.mention
    timestamp = datetime.now(pytz.timezone('asia/Jakarta')).strftime("%d-%m-%Y")
    jam = datetime.now(pytz.timezone('asia/Jakarta')).strftime("%H:%M:%S")

    try:
        x = await client.get_inline_bot_results(TB.me.username, "absen_in")
        if x.results:
            await message.reply_inline_bot_result(x.query_id, x.results[0].id)
        else:
            await message.reply("Tidak ada hasil inline bot.")
    except asyncio.TimeoutError:
        await message.reply("Waktu habis dalam mendapatkan hasil inline.")
    except Exception as e:
        await message.reply(f"Terjadi kesalahan: {e}")
