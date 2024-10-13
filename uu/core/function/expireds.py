import asyncio

from datetime import datetime
from pytz import timezone

from uu import *


async def expiredUbot(X):
    try:
        now = datetime.now(timezone("Asia/Jakarta"))
        time = now.strftime("%d-%m-%Y")
        exp = await DB.get_expired(X.me.id)
        
        if not exp:
            await DB.remove_ubot(X.me.id)
            await DB.remove_expired(X.me.id)
            await DB.remove_vars(X.me.id, "ultrapremium")
            await X.log_out()
            await TB.send_message(X.me.id, "<b>Userbot removed due to no expiration date!</b>")
            return

        exp = exp.strftime("%d-%m-%Y")
        
        if time == exp:
            await DB.remove_ubot(X.me.id)
            await DB.remove_expired(X.me.id)
            await DB.remove_vars(X.me.id, "ultrapremium")
            await X.log_out()
            await TB.send_message(X.me.id, "<b>Userbot Expired!</b>")
    except Exception as e:
        await DB.remove_ubot(X.me.id)
        await DB.remove_expired(X.me.id)
        await DB.remove_vars(X.me.id, "ultrapremium")
        await X.log_out()
        await TB.send_message(X.me.id, f"<b>Userbot Expired!</b>")

async def exp_ubot():
    while True:
        tasks = [expiredUbot(X) for X in TU._ubot]
        await asyncio.gather(*tasks)
        await asyncio.sleep(60)

