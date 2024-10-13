import re

from pyrogram.types import *

from uu import *


@PY.UBOT("help")
async def _(client, message):
    try:
        x = await client.get_inline_bot_results(TB.me.username, "user_help")
        await message.reply_inline_bot_result(x.query_id, x.results[0].id)
    except Exception as error:
        await message.reply(error)


@PY.INLINE("^user_help")
async def _(client, inline_query):
    Tk = await TU.get_pref(inline_query.from_user.id)
    msg = f"<b> Menu Help\n Prefixes: {' '.join(Tk)}</b>"
    results = [InlineQueryResultArticle(
        title="Menu Help",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Menu", callback_data="help_open")]]),
        input_message_content=InputTextMessageContent(f"Click the menu to display the features"),
    )]
    await client.answer_inline_query(inline_query.id, cache_time=60, results=results)



@PY.CALLBACK("help_(.*?)")
async def _(client, callback_query):
    try:
        mod_match = re.match(r"help_module\((.+?)\)", callback_query.data)
        prev_match = re.match(r"help_prev\((.+?)\)", callback_query.data)
        next_match = re.match(r"help_next\((.+?)\)", callback_query.data)
        back_match = re.match(r"help_back", callback_query.data)
        close_match = re.match(r"help_close", callback_query.data)
        open_match = re.match(r"help_open", callback_query.data)
        Tk = await TU.get_pref(callback_query.from_user.id)
        top_text = f"<b> Menu Help\n Prefixes: {' '.join(Tk)}</b>"

        if mod_match:
            module = (mod_match.group(1)).replace(" ", "_")
            text = HELP_COMMANDS[module].__HELP__.format(next((p) for p in Tk))
            button = [[InlineKeyboardButton(" Back ", callback_data="help_back")]]
            await callback_query.edit_message_text(
                text,
                reply_markup=InlineKeyboardMarkup(button),
                disable_web_page_preview=True,
            )
        elif prev_match:
            curr_page = int(prev_match.group(1))
            await callback_query.edit_message_text(
                top_text,
                reply_markup=InlineKeyboardMarkup(paginate_modules(curr_page - 1, HELP_COMMANDS, "help")),
                disable_web_page_preview=True,
            )
        elif next_match:
            next_page = int(next_match.group(1))
            await callback_query.edit_message_text(
                text=top_text,
                reply_markup=InlineKeyboardMarkup(paginate_modules(next_page + 1, HELP_COMMANDS, "help")),
                disable_web_page_preview=True,
            )
        elif back_match:
            await callback_query.edit_message_text(
                text=top_text,
                reply_markup=InlineKeyboardMarkup(paginate_modules(0, HELP_COMMANDS, "help")),
                disable_web_page_preview=True,
            )
        elif close_match:
            await callback_query.edit_message_text(
                text="Click the menu to display the features",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Menu", callback_data="help_open")]]),
            disable_web_page_preview=True
        )
        elif open_match:
            buttons = paginate_modules(0, HELP_COMMANDS, "help")
            await callback_query.edit_message_text(
                text=top_text,
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"[MyYuu]: {e}")
