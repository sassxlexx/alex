from uu import *

__MODULE__ = "setting"
__HELP__= """
<b>Menu Help!</b>

<b>Cek prefix ke bot nya</b>
 <code>/cekprefix</code>

<b>Set your prefix handler</b>
 <code>{0}setprefix</code>

<b>Query ping:</b>
  <code>|pong |owner |ubot</code>

<b>Ping</b>
 <code>{0}ping</code>

<b>Settings text ping</b>
  <code>settext [query] [text]</code>

<b>Type emoji:</b>
  <code>|pong |owner |ubot</code>

<b>Set your emoji</b>
 <code>{0}setemoji</code>

"""


@PY.BOT("cekprefix")
async def _(client, message):
    SH = await TU.get_pref(message.from_user.id)
    uu = await message.reply(f"Makanya kalau setprefix tu jangan ngasal !!! Bentar gw cek prefix lu...")
    await asyncio.sleep(5)
    await uu.delete()
    await message.reply(f"<b>Prefix: {' '.join(SH)}</b>")


@PY.UBOT("setprefix")
async def _(client, message):
    Tm = await message.reply("<b>Processing...</b>", quote=True)
    if len(message.command) < 2:
        return await Tm.edit(f"<code>{message.text}</code> <b>Prefix</b>")
    else:
        ub_prefix = []
        for prefix in message.command[1:]:
            if prefix.lower() == "none":
                ub_prefix.append("")
            else:
                ub_prefix.append(prefix)
        try:
            client.set_pref(message.from_user.id, ub_prefix)
            await DB.set_prefix(message.from_user.id, ub_prefix)
            parsed_prefix = " ".join(f"<code>{prefix}</code>" for prefix in ub_prefix)
            return await Tm.edit(f"<b>Prefix set to: {parsed_prefix}</b>")
        except Exception as error:
            return await Tm.edit(str(error))



mapping_query = {
    "pong": "PONG",
    "ubot": "UBOT",
    "owner": "OWNER",
    "proses": "PROSES",
    "sukses": "SUKSES",
}



@PY.UBOT("settext")
async def set_text_message(client: Client, message: Message):
    user_id = message.from_user.id
    args = message.text.split(maxsplit=2)
    if len(args) >= 3:
        command, new_message = args[1], args[2]
        if command in mapping_query:
            query = mapping_query[command]
            await DB.set_vars(client.me.id, query, Fonts.smallcap(new_message))
            await message.reply_text(f"<b>Berhasil mengubah text {command}</b>")
        else:
            await message.reply_text(f"<b>Query tidak di temukan!</b>")
    else:
        await message.reply_text(f"<b>{await EMO.GAGAL(client)} Tolong berikan query dan value!</b>")


@PY.UBOT("setemoji")
async def _(client, message):
    try:
        msg = await message.reply(f"<b>Processing...</b>", quote=True)

        if not client.me.is_premium:
            return await msg.edit(
                f"<b>Beli prem dulu!</b>"
            )

        if len(message.command) < 3:
            return await msg.edit(f"<b>Tolong masukan query dan value!</b>")

        query_mapping = {
          "pong": "EMOJI_PING",
          "owner": "EMOJI_MENTION",
          "ubot": "EMOJI_USERBOT",
        }
        command, mapping, value = message.command[:3]

        if mapping.lower() in query_mapping:
            query_var = query_mapping[mapping.lower()]
            emoji_id = None
            if message.entities:
                for entity in message.entities:
                    if entity.custom_emoji_id:
                        emoji_id = entity.custom_emoji_id
                        break

            if emoji_id:
                await DB.set_vars(client.me.id, query_var, emoji_id)
                await msg.edit(
                    f"<b>Emoji berhasil di settings ke:</b> <emoji id={emoji_id}>{value}</emoji>"
                )
            else:
                await msg.edit(f"<b>Tidak dapat menemukan emoji premium</b>")
        else:
            await msg.edit(f"<b>Mapping tidak ditemukan!</b>")

    except Exception as error:
        await msg.edit(str(error))

