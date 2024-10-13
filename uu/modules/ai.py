import os
import io
import base64

from PIL import Image, ImageDraw, ImageFont

from uu import *

__MODULE__ = "ChatGPT"
__HELP__ = """
<b>Menu ChatGPT!</b>

<b>Ask GPT a question!</b>
 <code>{0}ai or {0}ask</code>

<b>Make a picture!</b>(ultra)
 <code>{0}dalle</code>

<b>Change voice or audio to text!</b>(ultra)
 <code>{0}stt</code>
"""



@PY.UBOT("ask|ai")
async def chat_gpt(client, message):
    try:
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)

        if len(message.command) < 2:
            await message.reply_text(
                f"{message.text}</code> bagaimana membuat kue?"
            )
        else:
            prs = await message.reply_text(f"Proccesing....")
            a = message.text.split(' ', 1)[1]
            response = requests.get(f'https://widipe.com/openai?text={a}')

            try:
                if "result" in response.json():
                    x = response.json()["result"]                  
                    await prs.edit(
                      f"{x}\n\n<b>Dijawab Oleh:</b> {TB.me.mention}"
                    )
                else:
                    await message.reply_text("No 'results' key found in the response.")
            except KeyError:
                await message.reply_text("Error accessing the response.")
    except Exception as e:
        await message.reply_text(f"{e}")


@PY.UBOT("dalle")
@PY.ULTRA
async def _(client, message):
    Tm = await message.reply("<b>Peocessinh...</b>")
    if len(message.command) < 2:
        return await Tm.edit(f"<b>Provide description criteria!</b>")
    try:
        response = await OpenAi.ImageDalle(message.text.split(None, 1)[1])
        msg = message.reply_to_message or message
        await client.send_photo(message.chat.id, response, reply_to_message_id=msg.id)
        return await Tm.delete()
    except Exception as error:
        await message.reply(error)
        return await Tm.delete()


@PY.UBOT("stt")
@PY.ULTRA
async def _(client, message):
    Tm = await message.reply("<b>Processing...</b>")
    reply = message.reply_to_message
    if reply:
        if reply.voice or reply.audio or reply.video:
            file = await client.download_media(
                message=message.reply_to_message,
                file_name=f"sst_{message.reply_to_message.id}",
            )
            audio_file = f"{file}.mp3"
            cmd = f"ffmpeg -i {file} -q:a 0 -map a {audio_file}"
            await run_cmd(cmd)
            os.remove(file)
            try:
                response = await OpenAi.SpeechToText(audio_file)
            except Exception as error:
                await message.reply(error)
                return await Tm.delete()
            if int(len(str(response))) > 4096:
                with io.BytesIO(str.encode(str(response))) as out_file:
                    out_file.name = "openAi.txt"
                    await message.reply_document(
                        document=out_file,
                    )
                    return await Tm.delete()
            else:
                msg = message.reply_to_message or message
                await client.send_message(
                    message.chat.id, response, reply_to_message_id=msg.id
                )
                return await Tm.delete()
        else:
            return await Tm.edit(
                f"<b>Please reply media, audio, and voice!</b>"
            )
