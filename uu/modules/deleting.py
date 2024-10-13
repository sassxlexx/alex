from uu import *


__MODULE__ = "Deleting"
__HELP__ = """
<b>Menu Deleting!</b>

<b>Delete message!</b>
 <code>{0}del</code>

<b>Delete messages from those who reply!</b>
 <code>{0}purge</code>

<b>Delete your message</b>
 <code>{0}purgeme</code>
"""


@PY.UBOT("del")
async def _(client, message):
    msg_src = message.reply_to_message
    if msg_src:
        if msg_src.from_user.id:
            try:
                await client.delete_messages(message.chat.id, msg_src.id)
                await message.delete()
            except BaseException:
                pass
    else:
        await message.delete()


@PY.UBOT("purge")
async def _(client, message):
    Tk = await message.reply("<b>Starting to purge message!</b>")
    msg = message.reply_to_message
    if msg:
        itermsg = list(range(msg.id, message.id))
    else:
        await Tk.edit("<b>Reply to message for purge!</b>")
        return
    count = 0

    for i in itermsg:
        try:
            count = count + 1
            await client.delete_messages(
                chat_id=message.chat.id, message_ids=i, revoke=True
            )
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            await Tk.edit(f"<b>Error:</b> {e}")
            return

    done = await Tk.edit(
        f"<b>Fast purge completed!</b>"
    )
    await asyncio.sleep(2)
    await done.delete()


@PY.UBOT("purgeme")
async def _(client, message):
    if len(message.command) != 2:
        return await message.delete()
    n = message.text.split(None, 1)[1].strip()
    if not n.isnumeric():
        return await message.reply("<b>Please enter quantity!</b>")
    n = int(n)
    if n < 1:
        return await message.reply("<b>Enter the number of messages you want to delete!</b>")
    chat_id = message.chat.id
    message_ids = [
        m.id
        async for m in client.search_messages(
            chat_id,
            from_user="me",
            limit=n,
        )
    ]
    if not message_ids:
        return await message.reply("<b>Can't find message!</b>")
    to_delete = [message_ids[i : i + 99] for i in range(0, len(message_ids), 99)]
    for hundred_messages_or_less in to_delete:
        await client.delete_messages(
            chat_id=chat_id,
            message_ids=hundred_messages_or_less,
            revoke=True,
        )
    await message.delete()
