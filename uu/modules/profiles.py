from pyrogram import *

from uu import *



__MODULE__ = "Profile"
__HELP__ = """
<b>Menu Profile!</b>

<b>Set your first_name account!</b>
 <code>{0}setfname</code>

<b>Set your last_name account!</b>
 <code>{0}setlname</code>

<b>Set your bio account!</b>
 <code>{0}setbio</code>

<b>Block user telegram!</b>
 <code>{0}block</code>

<b>Unblock user telegram!</b>
 <code>{0}unblock</code>
"""


@PY.UBOT("setfname")
async def _(client, message):
    tex = await message.reply("<b>Processing...</b>")
    
    if len(message.command) == 1:
        return await tex.edit("<b>Provide text to change the first_name!</b>")
    
    elif len(message.command) > 1:
        name = message.text.split(None, 1)[1]
        try:
            await client.update_profile(first_name=name)
            await tex.edit(
                f"<b>Set first_name to:</b> {name}"
            )
        except Exception as e:
            await tex.edit(f"<b>Error:</b> <code>{e}</code>")
    else:
        return await tex.edit("<b>Provide text to change the first_name!</b>")


@PY.UBOT("setlname")
async def _(client, message):
    tex = await message.reply("<b>Processing...</b>")
    
    if len(message.command) == 1:
        return await tex.edit("<b>Provide text to change the last_name!</b>")
    
    elif len(message.command) > 1:
        name = message.text.split(None, 1)[1]
        try:
            await client.update_profile(last_name=name)
            await tex.edit(
                f"<b>Set last_name to:</b> {name}"
            )
        except Exception as e:
            await tex.edit(f"<b>Error:</b> <code>{e}</code>")
    else:
        return await tex.edit("<b>Provide text to change the lats_name!</b>")


@PY.UBOT("setbio")
async def _(client, message):
    tex = await message.reply("<b>Processing...</b>")
    
    if len(message.command) == 1:
        return await tex.edit("<b>Provide text to change the bio!</b>")
    
    elif len(message.command) > 1:
        bio = message.text.split(None, 1)[1]
        try:
            await client.update_profile(bio=bio)
            await tex.edit(
                f"<b>Set bio to:</b> {name}"
            )
        except Exception as e:
            await tex.edit(f"<b>Error:</b> <code>{e}</code>")
    else:
        return await tex.edit("<b>Provide text to change the bio!</b>")


@PY.UBOT("block")
async def _(client, message):
    user_id = await extract_user(message)
    tex = await message.reply("<b>Peocessing...</b>")
    if not user_id:
        return await tex.edit(f"<b>Reply to user or user_id!</b>")
    if user_id == client.me.id:
        return await tex.edit("<b>Can't block myself!</b>")
    await client.block_user(user_id)
    umention = (await client.get_users(user_id)).mention
    await tex.edit(f"<b>Succes block!</b> {umention}")


@PY.UBOT("unblock")
async def _(client, message):
    user_id = await extract_user(message)
    tex = await message.reply("<b>Processing...</b>")
    if not user_id:
        return await tex.edit(f"<b>Reply to user or user_id!</b>")
    if user_id == client.me.id:
        return await tex.edit("<b>I'm not distracted!</b>")
    await client.unblock_user(user_id)
    umention = (await client.get_users(user_id)).mention
    await tex.edit(f"<b>Succes unblock!</b> {umention}")

