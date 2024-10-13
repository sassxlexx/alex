from config import Config

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from pyrogram import *
from pyrogram.enums import *
from functools import wraps

from uu import *

async def if_sudo(_, client, message):
    sudo_users = await DB.get_list_vars(client.me.id, "sudo_users")
    is_user = message.from_user if message.from_user else message.sender_chat
    is_self = bool(message.from_user and message.from_user.is_self or getattr(message, "outgoing", False))
    return is_user.id in sudo_users or is_self

async def delmeus_chat(_, client, message):
    chat_ids = await DB.get_list_vars(client.me.id, "delmeus_user")
    is_user = message.from_user if message.from_user else message.sender_chat
    return is_user.id in chat_ids


async def update_cmd(user_id, command, field, increment=False):
    top = await DB.get_vars(user_id, command, field)
    new_value = int(top) + 1 if top and increment else 1
    await DB.set_vars(user_id, command, new_value, field)
    return new_value


class PY:
    @staticmethod
    def UBOT(command, additional_filters=None):
        def wrapper(func):
            if additional_filters is None:
                filter = filters.create(if_sudo)

            filters_combined = TU.cmd_pref(command) & filter
            if additional_filters:
                filters_combined &= additional_filters
                
            @TU.on_message(filters_combined)
            async def wrapped_func(client, message):
                cmd = message.command[0].lower()
                await update_cmd(TB.me.id, cmd, "top_cmd", increment=True)
                
                await func(client, message)
                
            return wrapped_func
            
        return wrapper

    @staticmethod
    def BOT(command, additional_filters=None):
        def wrapper(func):
            filters_combined = filters.command(command)
            if additional_filters:
                filters_combined &= additional_filters

            @TB.on_message(filters_combined)
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    def PM_PERMIT():
        def wrapper(func):
            @TU.on_message(
                filters.private
                & filters.incoming
                & ~filters.me
                & ~filters.bot
                & ~filters.via_bot
                & ~filters.service,
                group=69,
            )
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    def LOGS_PRIVATE():
        def wrapper(func):
            @TU.on_message(
                filters.private & ~filters.me & ~filters.bot & ~filters.service & filters.incoming,
                group=6,
            )
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    def LOGS_GROUP():
        def wrapper(func):
            @TU.on_message(
                filters.group & filters.incoming & filters.mentioned & ~filters.bot,
                group=8,
            )
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    def AFK():
        def wrapper(func):
            afk_check = (filters.mentioned | filters.private) & ~filters.bot & ~filters.me & filters.incoming

            @TU.on_message(afk_check, group=7)
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def NO_CMD_UBOT(result, TU):
        query_mapping = {
            "FILTERS_GC": {
                "query": (
                    filters.text
                    & ~filters.private                 
                    & ~filters.bot
                    & ~filters.me
                    & ~filters.via_bot
                    & ~filters.forwarded
                ),
                "group": 9,
            },
            "FILTERS_PV": {
                "query": (
                    filters.text
                    & ~filters.group
                    & ~filters.me
                    & ~filters.bot
                    & ~filters.via_bot
                    & ~filters.forwarded
                ),
                "group": 10,
            },
        }
        result_query = query_mapping.get(result)

        def decorator(func):
            if result_query:
                async def wrapped_func(client, message):
                    await func(client, message)

                TU.on_message(result_query["query"], group=int(result_query["group"]))(wrapped_func)
                return wrapped_func
            else:
                return func

        return decorator

        
    @staticmethod
    def INLINE(command):
        def wrapper(func):
            @TB.on_inline_query(filters.regex(command))
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def CALLBACK(command):
        def wrapper(func):
            @TB.on_callback_query(filters.regex(command))
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def PRIVATE(func):
        async def function(client, message):
            if not message.chat.type == ChatType.PRIVATE:
                return 
            await func(client, message)

        return function

    @staticmethod
    def GROUP(func):
        async def function(client, message):
            if message.chat.type not in (ChatType.GROUP, ChatType.SUPERGROUP):
                return 
            await func(client, message)

        return function

    @staticmethod
    def ULTRA(func):
        async def function(client, message):
            ultra_id = await DB.get_vars(client.me.id, "ultrapremium")

            if not ultra_id:
                return
        
            await func(client, message)

        return function

    @staticmethod
    def OWNER(func):
        async def function(client, message):
            user = message.from_user
            if user.id != Config.OWNER_ID:
                return 
            await func(client, message)

        return function

    @staticmethod
    def DELMEUS():
        def decorator(func):
            return TU.on_message(filters.create(delmeus_chat) & ~filters.private)(func)
        return decorator

    @staticmethod
    def START(func):
        async def function(client, message):
            seved_users = await DB.get_list_vars(client.me.id, "saved_users")
            user_id = message.from_user.id
            if user_id != Config.OWNER_ID:
                if user_id not in seved_users:
                    await DB.add_list_vars(client.me.id, "saved_users", user_id)
                user_link = f"<a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>"
                formatted_text = f"{user_link}\n\n<code>{message.text}</code>"
                buttons = [
                    [
                        InlineKeyboardButton(
                            "👤 ᴅᴀᴘᴀᴛᴋᴀɴ ᴘʀᴏғɪʟ 👤",
                            callback_data=f"profil {message.from_user.id}",
                        ),
                    ]
                ]
                await TB.send_message(
                    Config.OWNER_ID,
                    formatted_text,
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
            return await func(client, message)

        return function
