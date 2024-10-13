from config import Config

from uu import *


__MODULE__ = "Anti User"
__HELP__ = """
<b>Menu AntiUser!</b>

<b>Adding users to dor!</b>
 <code>{0}dor</code>

<b>Remove user from dor list!</b>
 <code>{0}undor</code>

<b>Get list dor</b>
 <code>{0}listdor</code>
"""


@PY.UBOT("dor")
async def _(client, message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply("<b>Reply to user/user_id</b>")

    if user_id == Config.OWNER_ID:
        return await message.reply("<b>The user is the owner!</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await message.reply(f"<b>Error: {error}</b>")
    
    mention = f"[{user.first_name} {user.last_name or ''}](tg://user?id={user.id})" if user else "."
    
    vars = await DB.get_list_vars(client.me.id, "delmeus_user")
    if user.id not in vars:
        await DB.add_list_vars(client.me.id, "delmeus_user", user.id)
        return await message.reply(f"{mention} <b>Successfully added user to blacklist!</b>")
    else:
        return await message.reply(f"{mention} <b>The user is already on blacklist!</b>")


@PY.UBOT("undor")
async def _(client, message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply("<b>Reply to user/user_id</b>")

    if user_id == Config.OWNER_ID:
        return await message.reply("<b>The user is the owner!</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await message.reply(f"<b>Error: {error}</b>")

    mention = f"[{user.first_name} {user.last_name or ''}](tg://user?id={user.id})" if user else "."
    
    vars = await DB.get_list_vars(client.me.id, "delmeus_user")
    if user.id in vars:
        await DB.remove_list_vars(client.me.id, "delmeus_user", user.id)
        return await message.reply(f"{mention} <b>Successfully removed user from blacklist!</b>")
    else:
        return await message.reply(f"{mention} <b>The user does not exist in blacklist!</b>")


@PY.UBOT("listdor")
async def _(client, message):
    delmeus = await DB.get_list_vars(client.me.id, "delmeus_user")
    delmeus_users = []

    for user_id in delmeus:
        try:
            user = await client.get_users(user_id)
            delmeus_users.append(
                f"<b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code></b>"
            )
        except Exception as e:
            delmeus_users.append(f"<b>{user_id}</b>")

    total_delmeus_users = len(delmeus_users)
    if delmeus_users:
        delmeus_list_text = "\n".join(delmeus_users)
        return await message.reply(
            f"<b>List Delmeus:\n\n{delmeus_list_text}\n\nTotal Dor: {total_delmeus_users}</b>"
        )
    else:
        return await message.reply("<b>Empty list!</b>")
      

@PY.DELMEUS()
async def _(client, message):
    try:
        await message.delete()
    except Exception as r:
        print(r)


