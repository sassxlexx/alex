import json

import requests
from pyrogram import filters
from uu import *

from . import *

__MODULE__ = "Adzan"
__HELP__ = """
<b>Menu Adzan!</b>

<b>Jadwal adzan!</b>
 <code>{0}adzan [Your City]</code>
"""


@PY.UBOT("adzan")
async def adzan_shalat(client: Client, message: Message):
    LOKASI = message.text.split(" ", 1)[1]
    if not LOKASI:
        await message.reply("<i>Please enter your city name</i>")
        return True
    url = f"http://muslimsalat.com/{LOKASI}.json?key=bd099c5825cbedb9aa934e255a81a5fc"
    request = requests.get(url)
    if request.status_code != 200:
        await message.reply(f"<b>Sorry didn't find the city<code>{LOKASI}</code>")
    result = json.loads(request.text)
    uu = f"""
Jadwal adzan hari ini
<b>Tanggal</b> <code>{result['items'][0]['date_for']}</code>
<b>ᴋᴏᴛᴀ</b> <code>{result['query']} | {result['country']}</code>

<b>Terbit  :</b> <code>{result['items'][0]['shurooq']}</code>
<b>Subuh :</b> <code>{result['items'][0]['fajr']}</code>
<b>Dzuhur :</b> <code>{result['items'][0]['dhuhr']}</code>
<b>Ashar  :</b> <code>{result['items'][0]['asr']}</code>
<b>Maghrib :</b> <code>{result['items'][0]['maghrib']}</code>
<b>Isya :</b> <code>{result['items'][0]['isha']}</code>
"""
    await message.reply(usu)