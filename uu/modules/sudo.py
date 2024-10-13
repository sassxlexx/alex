from uu import *

__MODULE__ = "Sudo"
__HELP__= """
<b>Menu Sudo!</b>

<b>Menambahkan pengguna sudo</b>
 <code>{0}addsudo</code>

<b>Menghapus pengguna sudo</b>
 <code>{0}delsudo</code>

<b>Daftar pengguna sudo</b>
 <code>{0}getsudo</code>
"""


@PY.UBOT("addsudo")
async def _(client, message):
    msg = await message.reply(f"<b>Processing...</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b><code>{message.text.split()[0]}</code> [ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ]</b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    sudo_users = await DB.get_list_vars(client.me.id, "sudo_users")

    if user.id in sudo_users:
        return await msg.edit(
            f"<b>[{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) Sudah dalam daftar sudo</b>"
        )

    try:
        await DB.add_list_vars(client.me.id, "sudo_users", user.id)
        return await msg.edit(
            f"<b>[{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) Berhasil ditambahkan ke daftar sudo</b>"
        )
    except Exception as error:
        return await msg.edit(error)


@PY.UBOT("delsudo")
async def _(client, message):
    msg = await message.reply(f"<b>Processing...</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b><code>{message.text.split()[0]}</code> [User id/Username]</b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    sudo_users = await DB.get_list_vars(client.me.id, "sudo_users")

    if user.id not in sudo_users:
        return await msg.edit(
            f"<b>[{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) Tidak ada dalam daftar sudo!</b>"
        )

    try:
        await DB.remove_list_vars(client.me.id, "sudo_users", user.id)
        return await msg.edit(
            f"<b>[{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) Berhasil di hapus dari daftar sudo!</b>"
        )
    except Exception as error:
        return await msg.edit(error)


@PY.UBOT("getsudo")
async def _(client, message):
    Sh = await message.reply("<b>Processing...</b>")
    sudo_users = await DB.get_list_vars(client.me.id, "sudo_users")

    if not sudo_users:
        return await Sh.edit(f"<b>Daftar sudo kosong</b>")

    sudo_list = []
    for user_id in sudo_users:
        try:
            user = await client.get_users(int(user_id))
            sudo_list.append(
                f"├ [{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code>"
            )
        except:
            continue

    if sudo_list:
        response = (
            f"<b>Daftar sudo:</b>\n"
            + "\n".join(sudo_list)
            + f"\n<b>Total sudo:</b> <code>{len(sudo_list)}</code>"
        )
        return await Sh.edit(response)
    else:
        return await Sh.edit("<b>Gagal mengambil daftar sudo!</b>")

