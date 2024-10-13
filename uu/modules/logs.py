from uu import *

__MODULE__ = "Logs"
__HELP__ = """
<b>Menu Logs!</b>

<b>Created a logs to view chats</b>
 <code>{0}logs</code>

<b>Example:</b>
 <code>on = activated logs</code>
 <code>off = deactivate logs</code>
 <code>none = deleted logs</code>
"""


async def send_log(client, chat_id, message, message_text, msg):
    try:
        await client.send_message(chat_id, message_text, disable_web_page_preview=True)
        await message.forward(chat_id)
    except Exception as error:
        print(f"[Kanaeru]: {msg} - {error}")


@PY.LOGS_PRIVATE()
async def _(client, message):
    logs = await DB.get_vars(client.me.id, "id_logs")
    on_logs = await DB.get_vars(client.me.id, "on_off_logs")

    if logs and on_logs:
        type = "Privated"
        user_link = f"[{message.from_user.first_name} {message.from_user.last_name or ''}](tg://user?id={message.from_user.id})"
        message_link = (
            f"tg://openmessage?user_id={message.from_user.id}&message_id={message.id}"
        )
        link = f"[KLIK DISINI]({message_link})"
        message_text = f"""
<b>Ada Pesan Masuk !!</b>

    <b>Tipe Pesan:</b> {type}
    <b>Link Pesan:</b> {link}
    
<b>Pesan dari user: {user_link}</b>

"""
        await send_log(client, int(logs), message, message_text, "LOGS_PRIVATE")


@PY.LOGS_GROUP()
async def _(client, message):
    logs = await DB.get_vars(client.me.id, "id_logs")
    on_logs = await DB.get_vars(client.me.id, "on_off_logs")

    if logs and on_logs:
        type = "Group"
        user_link = f"[{message.from_user.first_name} {message.from_user.last_name or ''}](tg://user?id={message.from_user.id})"
        message_link = message.link
        message_text = f"""
<b>Ada Pesan Masuk !!</b>

    <b>Type Pesan:</b> <code>{type}</code>
    <b>Link Pesan:</b> [KLIK DISINI]({message_link})
    
<b>Pesan dari user: {user_link}</b>
"""
        await send_log(client, int(logs), message, message_text, "LOGS_GROUP")


@PY.UBOT("logs")
async def _(client, message):
    if len(message.command) < 2:
        return await message.reply("<b>please read the rocks menu!</b>")

    query = {"on": True, "off": False, "none": False}
    command = message.command[1].lower()

    if not query:
        return await message.reply("<b>Invalid option</b>")

    value = query[command]
    vars = await DB.get_vars(client.me.id, "id_logs")

    if not vars:
        logs = await create_logs(client)
        await DB.set_vars(client.me.id, "id_logs", logs)

    if command == "none" and vars:
        try:
            await client.delete_channel(vars)
        except Exception:
            pass
        await DB.set_vars(client.me.id, "id_logs", value)

    await DB.set_vars(client.me.id, "on_off_logs", value)
    return await message.reply(f"<b>Logs in settings:</b> {value}")

