from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.raw.functions import Ping
from pytz import timezone

from config import Config
from uu import *
from time import time

import speedtest
import platform
import psutil
import asyncio

import os
import platform
import subprocess
import sys
import traceback


@PY.BOT("control")
@PY.OWNER
async def _(client, message):
    buttons = BTN.BOT_HELP(message)
    sh = await message.reply("<b>Menu control!</b>", reply_markup=InlineKeyboardMarkup(buttons))


@PY.CALLBACK("balik")
async def _(client, callback_query):
    buttons = BTN.BOT_HELP(callback_query)
    sh = await callback_query.message.edit("<b>Menu control!</b>", reply_markup=InlineKeyboardMarkup(buttons))


@PY.CALLBACK("reboot")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if not user_id == Config.OWNER_ID:
        return await callback_query.answer("ᴛᴏᴍʙᴏʟ ɪɴɪ ʙᴜᴋᴀɴ ᴜɴᴛᴜᴋ ʟᴜ", True)
    await callback_query.answer("System berhasil di restart", True)
    os.execl(sys.executable, sys.executable, "-m", "uu")


@PY.CALLBACK("update")
async def _(client, callback_query):
    out = subprocess.check_output(["git", "pull"]).decode("UTF-8")
    user_id = callback_query.from_user.id
    if not user_id == Config.OWNER_ID:
        return await callback_query.answer("Tombol ini bukan untuk anda", True)
    if "Already up to date." in str(out):
        return await callback_query.answer("Sudah versi terbaru", True)
    else:
        await callback_query.answer("Sedang memproses update...", True)
    os.execl(sys.executable, sys.executable, "-m", "uu")


@PY.CALLBACK("shutdown")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if not user_id == Config.OWNER_ID:
        return await callback_query.answer("Tombol ini bukan untuk anda", True)
    await callback_query.answer("System berhasil di matikan", True)
    os.system(f"kill -9 {os.getpid()}")

@PY.BOT("stats")
@PY.OWNER
async def _(client, message):
    xx = await message.reply("<b>Getting system stats...</b>")
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    end = datetime.now()
    delta_ping = (end - start).microseconds / 1000
    uptime = await get_time((time() - start_time))

    st = speedtest.Speedtest()
    st.download()
    st.upload()
    result = st.results.dict()
    download_speed = round(result["download"] / 10**6, 2)
    upload_speed = round(result["upload"] / 10**6, 2)
    ping_speed = round(result["ping"], 2)
    
    cpu = psutil.cpu_percent(interval=1)
    core = psutil.cpu_count(logical=True)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    process = psutil.Process(os.getpid())

    guest = await DB.get_list_vars(client.me.id, "start_users")
    total_guest = len(guest) if guest else 0
    
    _ping = f"""
<b>Kanaeru Info!!!</b>
  <code>Ping: {str(delta_ping).replace('.', ',')}ms
  Client: {len(TU._ubot)}
  User_start: {total_guest}
  Uptime: {uptime}
  Owner: @UsuReal022</code>

<b>Kanaeru System!!!</b>
  <code>Cpu: {cpu}%
  Core: {core}
  Ram: {ram}%
  Disk: {disk}%
  Memory: {round(process.memory_info()[0] / 1024 ** 2)} MB</code>
"""
    return await xx.edit(_ping)


@PY.CALLBACK("^profil")
async def _(client, callback_query):
    user_id = int(callback_query.data.split()[1])
    try:
        get = await TB.get_users(user_id)
        first_name = f"{get.first_name}"
        last_name = f"{get.last_name}"
        full_name = f"{get.first_name} {get.last_name or ''}"
        username = f"{get.username}"
        msg = (
            f"<b>👤 <a href=tg://user?id={get.id}>{full_name}</a></b>\n"
            f"<b> ┣ ID Pengguna:</b> <code>{get.id}</code>\n"
            f"<b> ┣ Nama Depan:</b> {first_name}\n"
        )
        if last_name == "None":
            msg += ""
        else:
            msg += f"<b> ┣ Nama Belakang:</b> {last_name}\n"
        if username == "None":
            msg += ""
        else:
            msg += f"<b> ┣ Username:</b> @{username}\n"
        msg += f"<b> ┗ ʙᴏᴛ: {TB.me.mention}\n"
        buttons = [
            [
                InlineKeyboardButton(
                    f"{full_name}",
                    url=f"tg://openmessage?user_id={get.id}",
                )
            ]
        ]
        await callback_query.message.reply_text(
            msg, reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as why:
        await callback_query.message.reply_text(why)


@PY.BOT("cek")
async def _(client, message):
    Sh = await message.reply(f"<b>Processing...</b>")
    user_id = await extract_user(message)
    if message.from_user.id == Config.OWNER_ID:
        pass
    elif message.from_user.id in await DB.get_list_vars(client.me.id, "seller_users"):
        pass
    else:
        return await Sh.edit("<b>You do not have access to use this command here</b>")

    if not user_id:
        return await Sh.edit("Pengguna tidak ditemukan!")
    try:
        get_exp = await DB.get_expired(user_id)
        sh = await client.get_users(user_id)
    except Exception as error:
        return await Sh.ediit(error)
    if get_exp is None:
        await Sh.edit(f"{user_id} Belum diaktifkan!")
    else:
        SH = await TU.get_pref(user_id)
        exp = get_exp.strftime("%d-%m-%Y")
        await Sh.edit(f"""
<b>Information!</b>
 <b>Name: {sh.mention}</b>
 <b>id:</b> {user_id}
 <b>prefix: {' '.join(SH)}</b>
 <b>expired: {exp}</b>
"""
        )



@PY.BOT("top")
@PY.OWNER
async def _(client, message):
    vars = await DB.all_vars(TB.me.id, "top_cmd") or {}
    sorted_vars = sorted(vars.items(), key=lambda item: item[1], reverse=True)

    command_count = 1000
    text = message.text.split()

    if len(text) == 2:
        try:
            command_count = min(max(int(text[1]), 1), 10)
        except Exception:
            pass

    total_count = sum(count for _, count in sorted_vars[:command_count])

    txt = "<b>Top Commnads!!!</b>\n\n"
    for command, count in sorted_vars[:command_count]:
        txt += f" {command}:<code>{count}</code>\n"

    txt += f"<b>\nTotal Commands:</b> <code>{total_count}</code>"

    return await message.reply(txt, quote=True)


@PY.BOT("addtime")
async def _(client, message):
    Tm = await message.reply("<b>Processing...</b>")
    user_id, get_day = await extract_user_and_reason(message)

    if message.from_user.id == Config.OWNER_ID:
        pass
    else:
        return await Tm.edit("<b>You do not have access to use this command here</b>")
    
    if not user_id:
        return await Tm.edit(f"<b>Provide user_id or username and day limit!</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await Tm.edit(str(error))

    get_day = get_day or 30
    now = datetime.now(timezone("Asia/Jakarta"))
    expire_date = now + timedelta(days=int(get_day))
    
    await DB.set_expired(user_id, expire_date)

    await Tm.edit(f"""
<b>Information!</b>
 <b>Name:</b> {user.mention}
 <b>Ids:</b> {user.id}
 <b>Active during:</b> {get_day} <b>day</b>
 <b>Expired:</b> {expire_date.strftime('%d-%m-%Y')}
""")


@PY.BOT("profile")
async def _(client, message):
    Sh = await message.reply("<b>Processing...</b>")
    user_id = await extract_user(message) or message.from_user.id
    if not user_id:
        return await Sh.edit("<b>User not found!</b>")
    try:
        get_exp = await DB.get_expired(user_id)
        sh = await client.get_users(user_id)
        SH = await TU.get_pref(user_id)
        exp = get_exp.strftime('%d-%m-%Y') if get_exp else "Null"
        st = "Running" if user_id in TU._get_my_id else "Stopped"
        if await DB.get_vars(user_id, "ultrapremium"):
            type = "Ultrapremium"
        else:
            type = "Premium"
        await Sh.edit(f"""
<b>Profiles!</b>
 <b>Plan:</b> {type} __{st}__
 <b>Name:</b> {sh.mention}
 <b>ids:</b> {user_id}
 <b>prefix:</b> {' '.join(SH)}
 <b>Expires on:</b> {exp}
""")
    except Exception as error:
        await Sh.edit(error)



@PY.BOT("addprem")
async def _(client, message):
    user_id, get_bulan = await extract_user_and_reason(message)
    msg = await message.reply("<b>Processing...</b>")
    if not user_id:
        return await msg.edit(f"<b>{message.text} user_id/reply</b>")
    if user_id in TU._get_my_id:
        return await msg.edit("<b>Users have used userbots!</b>")
    
    if message.from_user.id == Config.OWNER_ID:
        pass
    elif message.from_user.id in await DB.get_list_vars(client.me.id, "seller_users"):
        pass
    else:
        return await msg.edit("<b>You do not have access to use this command here</b>")
    
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"<b>Error: {error}</b>")
    
    acc_users = await DB.get_list_vars(client.me.id, "acc_users")
    if user.id in acc_users:
        return await msg.edit(f"""
<b>Information!</b>
 <b>Name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
 <b>id:</b> {user.id}
 <b>reason:</b> <code>already in list acces</code>
 <b>expired: <code>{get_bulan or 1}</code> month(s)</b>
        """)
    try:
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=int(get_bulan or 1))
        await DB.set_expired(user_id, expired)
        await DB.remove_vars(user_id, "ultrapremium")
        await DB.add_list_vars(TB.me.id, "acc_users", user.id)
        await msg.edit(f"""
<b>Information!</b>
 <b>Name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
 <b>id:</b> {user.id}
 <b>reason:</b> <code>Premium</code>
 <b>expired:</b> <code>{get_bulan or 1}</code> month(s)</b>
 <b>silahkan membuat userbot di @{TB.me.username}</b>
""")
        return await TB.send_message(
            Config.OWNER_ID,
            f"<b>Status: premium\n\n🆔 ID-Seller: {message.from_user.id}\n\n🆔 ID-Buyer: {user_id}</b>",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Seller",
                            callback_data=f"profil {message.from_user.id}",
                        ),
                        InlineKeyboardButton(
                            "Buyer", callback_data=f"profil {user_id}"
                        ),
                    ],
                ]
            ),
        )
    except Exception as error:
        return await msg.edit(error)


@PY.BOT("unprem")
async def _(client, message):
    msg = await message.reply("<b>Processing...</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"<b>{message.text} user_id/reply</b>")   
    if message.from_user.id == Config.OWNER_ID:
        pass
    elif message.from_user.id in await DB.get_list_vars(client.me.id, "seller_users"):
        pass
    else:
        return await msg.edit("<b>You do not have access to use this command here</b>")
    
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)
    acc_users = await DB.get_list_vars(client.me.id, "acc_users")
    if user.id not in acc_users:
        return await msg.edit(f"""
<b>Information!</b>
 <b>Name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
 <b>id:</b> {user.id}
 <b>reason:</b> <code>not in the list acces</code>
        """)
    
    await DB.remove_list_vars(client.me.id, "acc_users", user.id)
    await DB.remove_expired(user_id)
    await msg.edit(f"""
<b>Information!</b>
 <b>Name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
 <b>id:</b> {user.id}
 <b>reason:</b> <code>Unpremium</code>
    """)

@PY.BOT("addultra")
async def _(client, message):
    user_id, get_bulan = await extract_user_and_reason(message)
    msg = await message.reply("<b>Processing...</b>")
    if not user_id:
        return await msg.edit(f"<b>{message.text} user_id/reply</b>")
    if user_id in TU._get_my_id:
        return await msg.edit("<b>Users have used userbots!</b>")
    
    if message.from_user.id == Config.OWNER_ID:
        pass
    elif message.from_user.id in await DB.get_list_vars(client.me.id, "seller_users"):
        pass
    else:
        return await msg.edit("<b>You do not have access to use this command here</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"<b>Error: {error}</b>")
    
    acc_users = await DB.get_list_vars(client.me.id, "acc_users")
    if user.id in acc_users:
        return await msg.edit(f"""
<b>Information!</b>
 <b>Name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
 <b>id:</b> {user.id}
 <b>reason:</b> <code>already in list acces</code>
 <b>expired:</b> <code>{get_bulan or 1}</code> month(s)</b>
        """)
    try:
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=int(get_bulan or 1))
        await DB.set_expired(user_id, expired)
        await DB.set_vars(user_id, "ultrapremium", True)
        await DB.add_list_vars(TB.me.id, "acc_users", user.id)
        await msg.edit(f"""
<b>Information!</b>
 <b>Name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
 <b>id:</b> {user.id}
 <b>reason:</b> <code>Ultrapremium</code>
 <b>expired:</b> <code>{get_bulan or 1}</code> month(s)</b>
 <b>silahkan membuat userbot di @{TB.me.username}</b>
        """)
        return await TB.send_message(
            Config.OWNER_ID,
            f"<b>Status: ultra\n\n🆔 ID-Seller: {message.from_user.id}\n\n🆔 ID-Buyer: {user_id}</b>",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Seller",
                            callback_data=f"profil {message.from_user.id}",
                        ),
                        InlineKeyboardButton(
                            "Buyer", callback_data=f"profil {user_id}"
                        ),
                    ],
                ]
            ),
        )
    except Exception as error:
        return await msg.edit(error)


@PY.BOT("unultra")
async def _(client, message):
    msg = await message.reply("<b>Processing...</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"<b>{message.text} user_id/reply</b>")

    if message.from_user.id == Config.OWNER_ID:
        pass
    elif message.from_user.id in await DB.get_list_vars(client.me.id, "seller_users"):
        pass
    else:
        return await msg.edit("<b>You do not have access to use this command here</b>")
    
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)
    acc_users = await DB.get_list_vars(client.me.id, "acc_users")
    if user.id not in acc_users:
        return await msg.edit(f"""
<b>Information!</b>
 <b>Name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
 <b>id:</b> {user.id}
 <b>reason:</b> <code>not in the list</code>
        """)

    await DB.remove_vars(user_id, "ultrapremium")
    await DB.remove_list_vars(client.me.id, "acc_users", user.id)
    await DB.remove_expired(user_id)
    await msg.edit(f"""
<b>Information!</b>
 <b>Name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
 <b>id:</b> {user.id}
 <b>reason:</b> <code>Unultraprem</code>
    """)
    

@PY.BOT("getacces")
async def _(client, message):
    prem = await DB.get_list_vars(client.me.id, "acc_users")
    prem_users = []

    for user_id in prem:
        try:
            user = await client.get_users(user_id)
            prem_users.append(
                f"<b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code></b>"
            )
        except Exception as error:
            return await message.reply(str(error))

    total_prem_users = len(prem_users)
    if prem_users:
        prem_list_text = "\n".join(prem_users)
        return await message.reply(
            f"<b>List Acces:\n\n{prem_list_text}\n\nTotal Acces: {total_prem_users}</b>"
        )
    else:
        return await message.reply("<b>Empty list!</b>")


@PY.BOT("addseles")
@PY.OWNER
async def _(client, message):
    msg = await message.reply("<b>Processing...</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b>{message.text} user_id/reply</b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    sudo_users = await DB.get_list_vars(client.me.id, "seller_users")

    if user.id in sudo_users:
        return await msg.edit(f"""
<b>Information!</b>
 <b>Name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
 <b>id:</b> {user.id}
 <b>reason: <code>sudah seller</code></b>
"""
        )

    try:
        await DB.add_list_vars(client.me.id, "seller_users", user.id)
        return await msg.edit(f"""
<b>Information!</b>
 <b>Name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
 <b>id:</b> {user.id}
 <b>reason: <code>seller</code></b>
"""
        )
    except Exception as error:
        return await msg.edit(error)


@PY.BOT("unseles")
@PY.OWNER
async def _(client, message):
    msg = await message.reply("<b>Processing...</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b>{message.text} user_id/reply</b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    seles_users = await DB.get_list_vars(client.me.id, "seller_users")

    if user.id not in seles_users:
        return await msg.edit(f"""
<b>Information!</b>
 <b>Name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
 <b>id:</b> {user.id}
 <b>reason</b>: <code>tidak dalam daftar</code>
"""
        )

    try:
        await DB.remove_list_vars(client.me.id, "seller_users", user.id)
        return await msg.edit(f"""
<b>Information!</b>
 <b>Name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
 <b>id:</b> {user.id}
 <b>reason: <code>unseller</code></b>
"""
        )
    except Exception as error:
        return await msg.edit(error)


@PY.BOT("getseles")
@PY.OWNER
async def _(client, message):
    Sh = await message.reply("<b>Processing...</b>")
    seles_users = await DB.get_list_vars(client.me.id, "seller_users")

    if not seles_users:
        return await Sh.edit("<b>Empty list!</b>")

    seles_list = []
    for user_id in seles_users:
        try:
            user = await client.get_users(int(user_id))
            seles_list.append(
                f"<b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code></b>"
            )
        except:
            continue

    if seles_list:
        response = (
            "<b>Daftra Seller:</b>\n\n"
            + "\n".join(seles_list)
            + f"\n\n<b>Total Seller:</b> <code>{len(seles_list)}</code>"
        )
        return await Sh.edit(response)
    else:
        return await Sh.edit("<b>Unable to retrieve list!</b>")

#==============#

@PY.UBOT("addprem")
async def _(client, message):
    user_id, get_bulan = await extract_user_and_reason(message)
    msg = await message.reply("<b>Processing...</b>")
    if not user_id:
        return await msg.edit(f"<b>{message.text} user_id/reply</b>")
    if user_id in TU._get_my_id:
        return await msg.edit("<b>Users have used userbots!</b>")
    if message.from_user.id == Config.OWNER_ID:
        pass
    elif message.from_user.id in await DB.get_list_vars(TB.me.id, "seller_users"):
        pass
    else:
        return await msg.edit("<b>You do not have access to use this command here</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"<b>Error: {error}</b>")

    acc_users = await DB.get_list_vars(TB.me.id, "acc_users")
    if user.id in acc_users:
        return await msg.edit(f"""
<b>Information!</b>
 <b>Name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
 <b>id:</b> {user.id}
 <b>reason:</b> <code>already in list acces</code>
 <b>expired: <code>{get_bulan or 1}</code> month(s)</b>
        """)
    try:
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=int(get_bulan or 1))
        await DB.set_expired(user_id, expired)
        await DB.remove_vars(user_id, "ultrapremium")
        await DB.add_list_vars(TB.me.id, "acc_users", user.id)
        await msg.edit(f"""
<b>Information!</b>
 <b>Name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
 <b>id:</b> {user.id}
 <b>reason:</b> <code>Premium</code>
 <b>expired:</b> <code>{get_bulan or 1}</code> month(s)</b>
 <b>silahkan membuat userbot di @{TB.me.username}</b>
""")
        return await TB.send_message(
            Config.OWNER_ID,
            f"<b>Status: premium\n\n🆔 ID-Seller: {message.from_user.id}\n\n🆔 ID-Buyer: {user_id}</b>",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Seller",
                            callback_data=f"profil {message.from_user.id}",
                        ),
                        InlineKeyboardButton(
                            "Buyer", callback_data=f"profil {user_id}"
                        ),
                    ],
                ]
            ),
        )
    except Exception as error:
        return await msg.edit(error)



@PY.UBOT("unprem")
async def _(client, message):
    msg = await message.reply("<b>Processing...</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"<b>{message.text} user_id/reply</b>")

    if message.from_user.id == Config.OWNER_ID:
        pass
    elif message.from_user.id in await DB.get_list_vars(TV.me.id, "seller_users"):
        pass
    else:
        return await msg.edit("<b>You do not have access to use this command here</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)
    acc_users = await DB.get_list_vars(TB.me.id, "acc_users")
    if user.id not in acc_users:
        return await msg.edit(f"""
<b>Information!</b>
 <b>Name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
 <b>id:</b> {user.id}
 <b>reason:</b> <code>not in the list acces</code>
        """)

    await DB.remove_list_vars(TB.me.id, "acc_users", user.id)
    await DB.remove_expired(user_id)
    await msg.edit(f"""
<b>Information!</b>
 <b>Name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
 <b>id:</b> {user.id}
 <b>reason:</b> <code>Unpremium</code>
    """)

@PY.UBOT("addultra")
async def _(client, message):
    user_id, get_bulan = await extract_user_and_reason(message)
    msg = await message.reply("<b>Processing...</b>")
    if not user_id:
        return await msg.edit(f"<b>{message.text} user_id/reply</b>")
    if user_id in TU._get_my_id:
        return await msg.edit("<b>Users have used userbots!</b>")

    if message.from_user.id == Config.OWNER_ID:
        pass
    elif message.from_user.id in await DB.get_list_vars(TB.me.id, "seller_users"):
        pass
    else:
        return await msg.edit("<b>You do not have access to use this command here</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"<b>Error: {error}</b>")

    acc_users = await DB.get_list_vars(TB.me.id, "acc_users")
    if user.id in acc_users:
        return await msg.edit(f"""
<b>Information!</b>
 <b>Name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
 <b>id:</b> {user.id}
 <b>reason:</b> <code>already in list acces</code>
 <b>expired:</b> <code>{get_bulan or 1}</code> month(s)</b>
        """)
    try:
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=int(get_bulan or 1))
        await DB.set_expired(user_id, expired)
        await DB.set_vars(user_id, "ultrapremium", True)
        await DB.add_list_vars(TB.me.id, "acc_users", user.id)
        await msg.edit(f"""
<b>Information!</b>
 <b>Name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
 <b>id:</b> {user.id}
 <b>reason:</b> <code>Ultrapremium</code>
 <b>expired:</b> <code>{get_bulan or 1}</code> month(s)</b>
 <b>silahkan membuat userbot di @{TB.me.username}</b>
        """)
        return await TB.send_message(
            Config.OWNER_ID,
            f"<b>Status: ultra\n\n🆔 ID-Seller: {message.from_user.id}\n\n🆔 ID-Buyer: {user_id}</b>",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Seller",
                            callback_data=f"profil {message.from_user.id}",
                        ),
                        InlineKeyboardButton(
                            "Buyer", callback_data=f"profil {user_id}"
                        ),
                    ],
                ]
            ),
        )
    except Exception as error:
        return await msg.edit(error)


@PY.UBOT("unultra")
async def _(client, message):
    msg = await message.reply("<b>Processing...</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"<b>{message.text} user_id/reply</b>")

    if message.from_user.id == Config.OWNER_ID:
        pass
    elif message.from_user.id in await DB.get_list_vars(TB.me.id, "seller_users"):
        pass
    else:
        return await msg.edit("<b>You do not have access to use this command here</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)
    acc_users = await DB.get_list_vars(TB.me.id, "acc_users")
    if user.id not in acc_users:
        return await msg.edit(f"""
<b>Information!</b>
 <b>Name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
 <b>id:</b> {user.id}
 <b>reason:</b> <code>not in the list</code>
        """)

    await DB.remove_vars(user_id, "ultrapremium")
    await DB.remove_list_vars(TB.me.id, "acc_users", user.id)
    await DB.remove_expired(user_id)
    await msg.edit(f"""
<b>Information!</b>
 <b>Name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
 <b>id:</b> {user.id}
 <b>reason:</b> <code>Unultraprem</code>
    """)


@PY.UBOT("getacces")
async def _(client, message):
    prem = await DB.get_list_vars(TB.me.id, "acc_users")
    if message.from_user.id == Config.OWNER_ID:
        pass
    elif message.from_user.id in await DB.get_list_vars(TB.me.id, "seller_users"):
        pass
    else:
        return await msg.edit("<b>You do not have access to use this command here</b>")
    prem_users = []

    for user_id in prem:
        try:
            user = await client.get_users(user_id)
            prem_users.append(
                f"<b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code></b>"
            )
        except Exception as error:
            return await message.reply(str(error))

    total_prem_users = len(prem_users)
    if prem_users:
        prem_list_text = "\n".join(prem_users)
        return await message.reply(
            f"<b>List Acces:\n\n{prem_list_text}\n\nTotal Acces: {total_prem_users}</b>"
        )
    else:
        return await message.reply("<b>Empty list!</b>")


@PY.UBOT("addseles")
async def _(client, message):
    msg = await message.reply("<b>Processing...</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b>{message.text} user_id/reply</b>"
        )
    if message.from_user.id == Config.OWNER_ID:
        pass
    else:
        return await msg.edit("<b>You do not have access to use this command here</b>")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    sudo_users = await DB.get_list_vars(TB.me.id, "seller_users")

    if user.id in sudo_users:
        return await msg.edit(f"""
<b>Information!</b>
 <b>Name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
 <b>id:</b> {user.id}
 <b>reason: <code>sudah seller</code></b>
"""
        )

    try:
        await DB.add_list_vars(TB.me.id, "seller_users", user.id)
        return await msg.edit(f"""
<b>Information!</b>
 <b>Name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
 <b>id:</b> {user.id}
 <b>reason: <code>seller</code></b>
"""
        )
    except Exception as error:
        return await msg.edit(error)


@PY.UBOT("unseles")
async def _(client, message):
    msg = await message.reply("<b>Processing...</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b>{message.text} user_id/reply</b>"
        )
    if message.from_user.id == Config.OWNER_ID:
        pass
    else:
        return await msg.edit("<b>You do not have access to use this command here</b>")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    seles_users = await DB.get_list_vars(TB.me.id, "seller_users")

    if user.id not in seles_users:
        return await msg.edit(f"""
<b>Information!</b>
 <b>Name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
 <b>id:</b> {user.id}
 <b>reason</b>: <code>tidak dalam daftar</code>
"""
        )

    try:
        await DB.remove_list_vars(TB.me.id, "seller_users", user.id)
        return await msg.edit(f"""
<b>Information!</b>
 <b>Name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
 <b>id:</b> {user.id}
 <b>reason: <code>unseller</code></b>
"""
        )
    except Exception as error:
        return await msg.edit(error)


@PY.UBOT("getseles")
async def _(client, message):
    Sh = await message.reply("<b>Processing...</b>")
    seles_users = await DB.get_list_vars(TB.me.id, "seller_users")

    if not seles_users:
        return await Sh.edit("<b>Empty list!</b>")
    if message.from_user.id == Config.OWNER_ID:
        pass
    elif message.from_user.id in await DB.get_list_vars(TB.me.id, "seller_users"):
        pass
    else:
        return await msg.edit("<b>You do not have access to use this command here</b>")

    seles_list = []
    for user_id in seles_users:
        try:
            user = await client.get_users(int(user_id))
            seles_list.append(
                f"<b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code></b>"
            )
        except:
            continue

    if seles_list:
        response = (
            "<b>Daftra Seller:</b>\n\n"
            + "\n".join(seles_list)
            + f"\n\n<b>Total Seller:</b> <code>{len(seles_list)}</code>"
        )
        return await Sh.edit(response)
    else:
        return await Sh.edit("<b>Unable to retrieve list!</b>")


@PY.UBOT("top")
async def _(client, message):
    if message.from_user.id == Config.OWNER_ID:
        pass
    else:
        return await msg.edit("<b>You do not have access to use this command here</b>")
    vars = await DB.all_vars(TB.me.id, "top_cmd") or {}
    sorted_vars = sorted(vars.items(), key=lambda item: item[1], reverse=True)

    command_count = 1000
    text = message.text.split()

    if len(text) == 2:
        try:
            command_count = min(max(int(text[1]), 1), 10)
        except Exception:
            pass

    total_count = sum(count for _, count in sorted_vars[:command_count])

    txt = "<b>Top Commnads!!!</b>\n\n"
    for command, count in sorted_vars[:command_count]:
        txt += f" {command}:<code>{count}</code>\n"

    txt += f"<b>\nTotal Commands:</b> <code>{total_count}</code>"

    return await message.reply(txt, quote=True)


@PY.UBOT("addtime")
async def _(client, message):
    Tm = await message.reply("<b>Processing...</b>")
    user_id, get_day = await extract_user_and_reason(message)

    if message.from_user.id == Config.OWNER_ID:
        pass
    else:
        return await Tm.edit("<b>You do not have access to use this command here</b>")
    
    if not user_id:
        return await Tm.edit(f"<b>Provide user_id or username and day limit!</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await Tm.edit(str(error))

    get_day = get_day or 30
    now = datetime.now(timezone("Asia/Jakarta"))
    expire_date = now + timedelta(days=int(get_day))
    
    await DB.set_expired(user_id, expire_date)

    await Tm.edit(f"""
<b>Information!</b>
 <b>Name:</b> {user.mention}
 <b>Id:</b> {user.id}
 <b>Active during:</b> {get_day} <b>day</b>
 <b>Expired:</b> {expire_date.strftime('%d-%m-%Y')}
""")


@PY.UBOT("cek")
async def _(client, message):
    Sh = await message.reply(f"<b>Processing...</b>")
    user_id = await extract_user(message)
    if message.from_user.id == Config.OWNER_ID:
        pass
    elif message.from_user.id in await DB.get_list_vars(TB.me.id, "seller_users"):
        pass
    else:
        return await Sh.edit("<b>You do not have access to use this command here</b>")

    if not user_id:
        return await Sh.edit("Pengguna tidak ditemukan!")
    try:
        get_exp = await DB.get_expired(user_id)
        sh = await client.get_users(user_id)
    except Exception as error:
        return await Sh.ediit(error)
    if get_exp is None:
        await Sh.edit(f"{user_id} Belum diaktifkan!")
    else:
        SH = await TU.get_pref(user_id)
        exp = get_exp.strftime("%d-%m-%Y")
        await Sh.edit(f"""
<b>Information!</b>
 <b>Name: {sh.mention}</b>
 <b>id:</b> {user_id}
 <b>prefix: {' '.join(SH)}</b>
 <b>expired: {exp}</b>
"""
        )