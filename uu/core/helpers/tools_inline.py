import re
import base64

from struct import unpack
from base64 import urlsafe_b64decode
from attrify import Attrify as Atr

from pykeyboard import InlineKeyboard

from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from uu import *


def unpackInlineMessage(inline_message_id: str):
    dc_id, message_id, chat_id, query_id = unpack(
        "<iiiq",
        urlsafe_b64decode(
            inline_message_id + "=" * (len(inline_message_id) % 4),
        ),
    )
    temp = {
        "dc_id": dc_id,
        "message_id": message_id,
        "chat_id": int(str(chat_id).replace("-1", "-1001")),
        "query_id": query_id,
        "inline_message_id": inline_message_id,
    }
    return Atr(temp)


def detect_url_links(text):
    link_pattern = (
        r"(?:https?://)?(?:www\.)?[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+(?:[/?]\S+)?"
    )
    link_found = re.findall(link_pattern, text)
    return link_found


def detect_button_and_text(text):
    button_matches = re.findall(r"\| ([^|]+) - ([^|]+) \|", text)
    text_matches = (
        re.search(r"(.*?) \|", text, re.DOTALL).group(1) if "|" in text else text
    )
    return button_matches, text_matches


def create_inline_keyboard(text, user_id=False, is_back=False):
    keyboard = []
    button_matches, text_matches = detect_button_and_text(text)

    prev_button_data = None
    for button_text, button_data in button_matches:
        data = (
            button_data.split(";same")[0]
            if detect_url_links(button_data.split(";same")[0])
            else f"_gtnote {int(user_id.split('_')[0])}_{user_id.split('_')[1]} {button_data.split(';same')[0]}"
        )
        cb_data = data if user_id else button_data.split(";same")[0]
        if ";same" in button_data:
            if prev_button_data:
                if detect_url_links(cb_data):
                    keyboard[-1].append(InlineKeyboardButton(button_text, url=cb_data))
                else:
                    keyboard[-1].append(
                        InlineKeyboardButton(button_text, callback_data=cb_data)
                    )
            else:
                if detect_url_links(cb_data):
                    button_row = [InlineKeyboardButton(button_text, url=cb_data)]
                else:
                    button_row = [
                        InlineKeyboardButton(button_text, callback_data=cb_data)
                    ]
                keyboard.append(button_row)
        else:
            if button_data.startswith("http"):
                button_row = [InlineKeyboardButton(button_text, url=cb_data)]
            else:
                button_row = [InlineKeyboardButton(button_text, callback_data=cb_data)]
            keyboard.append(button_row)

        prev_button_data = button_data

    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    if user_id and is_back:
        markup.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    "back",
                    f"_gtnote {int(user_id.split('_')[0])}_{user_id.split('_')[1]}",
                )
            ]
        )

    return markup, text_matches


def ikb(rows=[]):
    lines = []
    for row in rows:
        line = []
        for button_data in row:
            if isinstance(button_data, str):
                match = re.match(r"\| ([^|]+) - ([^|]+) \|", button_data)
                if match:
                    text, action = match.groups()
                    button = InlineKeyboardButton(text=text.strip(), url=action.strip() if action.startswith("http") else None, callback_data=action.strip() if not action.startswith("http") else None)
                    line.append(button)
                else:
                    raise ValueError("Invalid button data format.")
            elif isinstance(button_data, tuple) and len(button_data) == 2:
                button = InlineKeyboardButton(text=button_data[0], url=button_data[1] if isinstance(button_data[1], str) and button_data[1].startswith("http") else None, callback_data=button_data[1] if isinstance(button_data[1], str) and not button_data[1].startswith("http") else None)
                line.append(button)
            else:
                raise ValueError("Invalid button data format.")
        lines.append(line)
    return InlineKeyboardMarkup(inline_keyboard=lines)


class BTN:
    def ALIVE(get_id):
        button = [
            [
                InlineKeyboardButton(
                    text="close",
                    callback_data=f"alv_cls {int(get_id[1])} {int(get_id[2])}",
                )
            ]
        ]
        return button
    
    def BOT_HELP(message):
        button = [
            [InlineKeyboardButton("Restart", callback_data="reboot")],

[InlineKeyboardButton("Shutdown", callback_data="shutdown")],
            [InlineKeyboardButton("Update", callback_data="update")],
        ]
        return button

    def START(message):
        button = ikb([
            ["| Create UserBot - bahan_ubot |"],
            [
              "| Status - status |",
              "| Owner - https://t.me/myYuuaja |",
            ],
            [
              "| Channel - https://t.me/Myuuser |",
            ],
        ])
        return button

    def UBOT(user_id, count):
        button = [
            [
                InlineKeyboardButton(
                    "📁 ʜᴀᴘᴜꜱ ᴅᴀʀɪ ᴅᴀᴛᴀʙᴀꜱᴇ 📁",
                    callback_data=f"del_ubot {int(user_id)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "⏳ ᴄᴇᴋ ᴋᴀᴅᴀʟᴜᴀʀꜱᴀ ⏳",
                    callback_data=f"cek_masa_aktif {int(user_id)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "🔑 ᴄᴇᴋ ᴏᴛᴘ 🔑",
                    callback_data=f"get_otp {int(count)}",
                )
            ],
            [
                InlineKeyboardButton("◄", callback_data=f"p_ub {int(count)}"),
                InlineKeyboardButton("►", callback_data=f"n_ub {int(count)}"),
            ],  
        ]
        return button

    def DEAK(user_id, count):
        button = [
            [
                InlineKeyboardButton(
                    "🔙 ᴋᴇᴍʙᴀʟɪ",
                    callback_data=f"p_ub {int(count)}"
                ),
                InlineKeyboardButton(
                    "sᴇᴛᴜJᴜɪ ✅", callback_data=f"deak_akun {int(count)}",
                ),
            ],
        ]
        return button
