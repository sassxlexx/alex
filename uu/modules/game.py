from uu import *

__MODULE__ = "Game"
__HELP__ = """
<b>Menu Games!</b>

<b>the game of chess</b>
 <code>{0}catur</code>
   
  """


@PY.UBOT("catur")
async def _(client, message):
    try:
        x = await client.get_inline_bot_results("GameFactoryBot")
        msg = message.reply_to_message or message
        await client.send_inline_bot_result(
            message.chat.id, x.query_id, x.results[0].id, reply_to_message_id=msg.id
        )
    except Exception as error:
        await message.reply(error)
