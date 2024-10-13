from gc import get_objects

from pyrogram.types import *

from uu import *


FLOOD = {}
MSG_ID = {}
PM_TEXT = """
<b>Hello {mention} can I help you?

Let me introduce myself as pm-security here!
Please wait until the user responds to your message and do not spam

Warning!: {warn}</b>
"""


__MODULE__ = "Pm Permit"
__HELP__ = """
<b>Menu Pm Permit!</b>

<b>Turn pmpermit on and off!</b>(ultra)
 <code>{0}pmpermit</code>

<b>Settings for pmpermit!</b>(ultra)
 <code>{0}setpm</code>

<b>Accept users to interact!</b>(ultra)
 <code>{0}ok or {0}approve</code>

<b>Prohibit users from interacting with us!</b>(ultra)
 <code>{0}no or {0}unapprove</code>

<b>Example Settings!</b>
 <code>text = Set text pm permit</code>
 <code>limit = Set limit warn pm permit</code>
"""


@PY.PM_PERMIT()
async def _(client, message):
    user = message.from_user
    pm_on = await DB.get_vars(client.me.id, "pm_permit")
    if pm_on:
        if user.id in MSG_ID:
            await delete_old_message(message, MSG_ID.get(user.id, 0))
        
        check = await DB.get_pm()
        if user.id not in check:
            FLOOD[user.id] = FLOOD.get(user.id, 0) + 1
            pm_limit = await DB.get_vars(client.me.id, "pm_limit") or "5"
            
            if FLOOD[user.id] > int(pm_limit):
                del FLOOD[user.id]
                await message.reply("<b>You have been blocked for spamming!</b>")
                return await client.block_user(user.id)
            
            pm_msg = await DB.get_vars(client.me.id, "pm_text") or PM_TEXT
            
            try:
                x = await client.get_inline_bot_results(
                    TB.me.username, f"pm_pr {id(message)} {FLOOD[user.id]}"
                )
                msg = await client.send_inline_bot_result(
                    message.chat.id,
                    x.query_id,
                    x.results[0].id,
                    reply_to_message_id=message.id,
                )
                MSG_ID[user.id] = int(msg.updates[0].id)
            except Exception as e:
                await message.reply(f"<b>Error:</b> {str(e)}")
        else:
            pass
                

@PY.INLINE("pm_pr")
async def _(client, inline_query):
    get_id = inline_query.query.split()
    m = next((obj for obj in get_objects() if id(obj) == int(get_id[1])), None)
    pm_msg = await DB.get_vars(m._client.me.id, "pm_text") or PM_TEXT
    pm_limit = await DB.get_vars(m._client.me.id, "pm_limit") or 5
    rpk = f"[{m.from_user.first_name} {m.from_user.last_name or ''}](tg://user?id={m.from_user.id})"
    peringatan = f"{int(get_id[2])} / {pm_limit}"
    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Approve!", callback_data=f"apprv_usr{m.from_user.id}")]]
    )
    text = pm_msg
    hasil = [
        InlineQueryResultArticle(
            title="Dapatkan tombol!",
            reply_markup=buttons,
            input_message_content=InputTextMessageContent(text.format(mention=rpk, warn=peringatan)),
        )
    ]
    
    await client.answer_inline_query(inline_query.id, cache_time=0, results=hasil)


@PY.UBOT("setpm")
@PY.ULTRA
async def _(client, message):
    if len(message.command) < 3:
        return await message.reply(
            f"<b>Enter the query and value correctly!</b>"
        )
    query = {"limit": "pm_limit", "text": "pm_text"}
    querys = message.command[1].lower()
    if querys not in query:
        return await message.reply("<b>The query you entered is invalid!</b>")
    query_str, value_str = (
        message.text.split(None, 2)[1],
        message.text.split(None, 2)[2],
    )
    value = query[query_str]
    if value_str.lower() == "none":
        value_str = False
    await DB.set_vars(client.me.id, value, value_str)
    return await message.reply(
        f"<b>PMpermit settings have been updated!</b>"
    )


@PY.UBOT("pmpermit")
@PY.ULTRA
async def _(client, message):
    if len(message.command) < 2:
        return await message.reply(
            f"<b>Usage on or off!</b>"
        )

    toggle_options = {"off": False, "on": True}
    toggle_option = message.command[1].lower()

    if toggle_option not in toggle_options:
        return await message.reply("<b>Invalid option!\nPlease use on or off!</b>")

    value = toggle_options[toggle_option]
    text = "Enable" if value else "Disable"

    await DB.set_vars(client.me.id, "pm_permit", value)
    await message.reply(f"<b>Pm permit successful {text}</b>")


@PY.CALLBACK("apprv_usr")
async def _(clinet, callback_query):
    data = callback_query.data
    try:
        user_id = int(data.split("usr")[-1])
    except ValueError:
        return await callback_query.answer("Invalid user ID", show_alert=True)

    if user_id:
        return await callback_query.answer("This button is not for you", show_alert=True)

    vars = await DB.get_pm()

    if user_id not in vars:
        await DB.approve_pm(user_id)
        await callback_query.answer("User accepted!", show_alert=True)
    else:
        await callback_query.answer("The user has been accepted previously!", show_alert=True)


@PY.UBOT("ok|approve")
@PY.ULTRA
@PY.PRIVATE
async def _(client, message):
    user = message.chat
    rpk = f"[{user.first_name} {user.last_name or ''}](tg://user?id={user.id})"
    vars = await DB.get_pm()
    if user.id not in vars:
        await DB.approve_pm(user.id)
        return await message.reply(f"<b>Okay, {rpk} received</b>")
    else:
        return await message.reply(f"<b>{rpk} already received</b>")


@PY.UBOT("no|disapprove")
@PY.ULTRA
@PY.PRIVATE
async def _(client, message):
    user = message.chat
    rpk = f"[{user.first_name} {user.last_name or ''}](tg://user?id={user.id})"
    vars = await DB.get_pm()
    if user.id not in vars:
        await message.reply(f"<b>Sorry, ⁣{rpk} you've been turned around</b>")
        return await client.block_user(user.id)
    else:
        await DB.disapprove_pm(user.id)
        return await message.reply(
            f"<b>Sorry, {rpk} You have been refused access to this account</b>"
        )


async def delete_old_message(message, msg_id):
    try:
        await message._client.delete_messages(message.chat.id, msg_id)
    except:
        pass
