from pyrogram.types import Message
from uu import *

import glob
import io
import os
import re
import urllib
import urllib.request

import bs4
import requests
from PIL import Image
from search_engine_parser import GoogleSearch

import urllib.parse

__MODULE__ = "Google"
__HELP__ = """
<b>Menu Google</b>

<b>Google search!</b>
 <code>{0}google</code> [Pertanyaan]
"""


opener = urllib.request.build_opener()
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
opener.addheaders = [("User-agent", useragent)]

@PY.UBOT("google")
async def gsearch(client, message):
    uu = await message.reply("Searching...")
    match = get_arg(message)
    if not match:
        await uu.edit("Berikan saya sesuatu...")
        return
    page = re.findall(r"page=\d+", match)
    try:
        page = page[0]
        page = page.replace("page=", "")
        match = match.replace("page=" + page[0], "")
    except IndexError:
        page = 1
    search_args = (str(match), int(page))
    gsearch = GoogleSearch()
    gresults = await gsearch.async_search(*search_args)
    msg = ""
    for i in range(len(gresults["links"])):
        try:
            title = gresults["titles"][i]
            link = gresults["links"][i]
            desc = gresults["descriptions"][i]
            msg += f"- [{title}]({link})\n**{desc}**\n\n"
        except IndexError:
            break
    await uu.edit(
        "**Permintaan pencarian:**\n`" + match + "`\n\n**Hasil pencarian:**\n" + msg)