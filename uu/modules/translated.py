from gpytranslate import Translator
from pyrogram import *
from pyrogram.types import *

from uu import *

__MODULE__ = "Translate"
__HELP__ = """
<b>Menu Translated!</b>

<b>Translates to language!</b>
 <code>{0}tr</code>
"""


@PY.UBOT("tr")
async def _(client, message):
    trl = Translator()

    if not message.reply_to_message:
        return await message.reply("<b>No message to translate.</b>")

    text = message.reply_to_message.text or message.reply_to_message.caption

    if not text:
        return await message.reply("<b>No text found in the message.</b>")

    input_str = message.text.split(None, 1)[1] if len(message.command) > 1 else None
    target = input_str or "id"

    try:
        tekstr = await trl(text, targetlang=target)
        detected_lang = await trl.detect(text)
    except ValueError as err:
        return await message.reply("<b>Error occurred during translation.</b>")

    reply_text = (
        f"<b>Translated to:</b> <code>{target}\n{tekstr.text}</code>\n\n"
        f"<b>Detected Language:</b> <code>{detected_lang}</code>"
    )

    await message.reply(reply_text)
