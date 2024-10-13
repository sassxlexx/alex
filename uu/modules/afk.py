from uu import *

__MODULE__ = "Afk"
__HELP__ = """
<b>Menu Afk!</b>

<b>Do afk!</b>
 <code>{0}afk</code>

<b>Do unafk!</b>
 <code>{0}unafk</code>
"""


@PY.UBOT("afk")
async def _(client, message):
    reason = get_arg(message)
    db_afk = {"time": time(), "reason": reason}
    msg_afk = (
        f"<b>Currently Afk!\nReason: {reason}</b>"
        if reason
        else "<b>Currently Afk!</b>"
      )
    await DB.set_vars(client.me.id, "afk", db_afk)
    return await message.reply(msg_afk)



@PY.AFK()
async def _(client, message):
    vars = await DB.get_vars(client.me.id, "afk")
    if vars:
        afk_time = vars.get("time")
        afk_reason = vars.get("reason")
        afk_runtime = await get_time(time() - afk_time)
        afk_text = (
            f"<b>Currently Afk!\nTime: {afk_runtime}\nReason: {afk_reason}</b>"
            if afk_reason
            else f"<b>Currently Afk!\nTime: {afk_runtime}</b>"
        )
        return await message.reply(afk_text)


@PY.UBOT("unafk")
async def _(client, message):
    vars = await DB.get_vars(client.me.id, "afk")
    if vars:
        afk_time = vars.get("time")
        afk_runtime = await get_time(time() - afk_time)
        afk_text = f"<b>Back Online!\nAFK during: {afk_runtime}</b>"
        await message.reply(afk_text)
        return await DB.remove_vars(client.me.id, "afk")
