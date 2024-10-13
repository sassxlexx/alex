from pyrogram.types import *

from uu import *

__MODULE__ = "Notes"
__HELP__ = """
<b>Menu Notes!</b>

<b>Saved notes!</b>
 <code>{0}addnote</code>

<b>Deleted notes!</b>
 <code>{0}delnote</code>

<b>Getting your notes!</b>
 <code>{0}get</code>

<b>list notes!</b>
 <code>{0}listnote</code>

<b>Example button!</b>
 <code>Hay sir | button_1 - #callback |</code>
"""


@PY.UBOT("addnote")
async def _(client, message):
    args = get_arg(message)
    reply = message.reply_to_message
    query = "notes_btn" if "#" in message.text else "notes_xx"

    if not args or not reply:
        return await message.reply(
            f"<b>Can't saved notes!</b>"
        )

    vars = await DB.get_vars(client.me.id, args, query)

    if vars:
        return await message.reply(f"<b>Notes <code>{args}</code> already available</b>")

    value = None
    type_mapping = {
        "text": reply.text,
        "photo": reply.photo,
        "voice": reply.voice,
        "audio": reply.audio,
        "video": reply.video,
        "animation": reply.animation,
        "sticker": reply.sticker,
    }

    for media_type, media in type_mapping.items():
        if media:
            send = await reply.copy(client.me.id)
            value = {
                "type": media_type,
                "message_id": send.id,
            }
            break

    if value:
        await DB.set_vars(client.me.id, args, value, query)
        return await message.reply(
            f"<b>Notes <code>{args}</code> saved successfully</b>"
        )
    else:
        return await message.reply(
            f"<b>Can't save notes!</b>"
        )


@PY.UBOT("delnote")
async def _(client, message):
    args = get_arg(message)

    if not args:
        return await message.reply(
            f"<b>Can't deleted notes!</b>"
        )

    query = "notes_btn" if "#" in message.text else "notes_xx"
    vars = await DB.get_vars(client.me.id, args, query)
    is_logs = await DB.get_vars(client.me.id, "id_logs")

    if not vars:
        return await message.reply(f"<b>Notes <code>{args}</code> can't find!</b>")

    await DB.remove_vars(client.me.id, args, query)
    await client.delete_messages(client.me.id, int(vars["message_id"]))
    return await message.reply(f"<b>Notes <code>{args}</code> successfully deleted</b>")


@PY.UBOT("get")
async def _(client, message):
    msg = message.reply_to_message or message
    args = get_arg(message)

    if not args:
        return await message.reply(
            f"<b>Notes named not found!</b>"
        )

    data = await DB.get_vars(client.me.id, args, "notes_xx")

    if not data:
        return await message.reply(
            f"<b>Notes {args} not found!</b>"
        )

    m = await client.get_messages(client.me.id, int(data["message_id"]))

    if data["type"] == "text":
        if matches := re.findall(r"\| ([^|]+) - ([^|]+) \|", m.text):
            try:
                x = await client.get_inline_bot_results(
                    TB.me.username, f"get_notes {client.me.id} {args}"
                )
                return await client.send_inline_bot_result(
                    message.chat.id,
                    x.query_id,
                    x.results[0].id,
                    reply_to_message_id=msg.id,
                )
            except Exception as error:
                await message.reply(error)
        else:
            return await m.copy(message.chat.id, reply_to_message_id=msg.id)
    else:
        return await m.copy(message.chat.id, reply_to_message_id=msg.id)


@PY.UBOT("listnote")
async def _(client, message):
    vars_cb = await DB.all_vars(client.me.id, "notes_btn")
    vars_notes = await DB.all_vars(client.me.id, "notes_xx")
    vars_combined = {**vars_cb, **vars_notes}
    
    if vars_combined:
        msg = "<b>List Notes!</b>\n\n"
        for x, data in vars_combined.items():
            msg += f" {x} |({data['type']})\n"
        msg += f"<b>\nTotal Notes: {len(vars_combined)}</b>"
    else:
        msg = "<b>Not list notes!</b>"

    return await message.reply(msg, quote=True)


@PY.INLINE("^get_notes")
async def _(client, inline_query):
    query = inline_query.query.split()
    data = await DB.get_vars(int(query[1]), query[2], "notes_xx")
    item = [x for x in TU._ubot if int(query[1]) == x.me.id]
    for me in item:
        m = await me.get_messages(int(me.me.id), int(data["message_id"]))
        buttons, text = create_inline_keyboard(m.text, f"{int(query[1])}_{query[2]}")
        return await client.answer_inline_query(
            inline_query.id,
            cache_time=0,
            results=[
                (
                    InlineQueryResultArticle(
                        title="get notes!",
                        reply_markup=buttons,
                        input_message_content=InputTextMessageContent(text),
                    )
                )
            ],
        )


@PY.CALLBACK("_gtnote")
async def _(client, callback_query):
    _, user_id, *query = callback_query.data.split()
    data_key = "notes_btn" if bool(query) else "notes_xx"
    query_eplit = query[0] if bool(query) else user_id.split("_")[1]

    data = await DB.get_vars(int(user_id.split("_")[0]), query_eplit, data_key)
    item = [x for x in TU._ubot if int(user_id.split("_")[0]) == x.me.id]

    if not data:
        return await callback_query.answer("Can not be found!", True)

    for me in item:
        m = await me.get_messages(int(me.me.id), int(data["message_id"]))
        buttons, text = create_inline_keyboard(
            m.text, f"{int(user_id.split('_')[0])}_{user_id.split('_')[1]}", bool(query)
        )
        return await callback_query.edit_message_text(text, reply_markup=buttons)
