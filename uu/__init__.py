import uvloop

uvloop.install()

import logging
import os

from pyrogram import *
from pyrogram.handlers import CallbackQueryHandler, MessageHandler
from pyrogram.types import Message
from pyromod import listen
from rich.logging import RichHandler
from pytgcalls import PyTgCalls
from pytgcalls import filters as fl
from aiohttp import ClientSession

from config import Config


class ConnectionHandler(logging.Handler):
    def emit(self, record):
        error_types = ["OSError", "TimeoutError"]
        if any(error_type in record.getMessage() for error_type in error_types):
            os.system(f"kill -9 {os.getpid()} && python3 -m uu")

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

formatter = logging.Formatter("[%(levelname)s] - %(name)s - %(message)s", "%d-%b %H:%M")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(ConnectionHandler())





class Bot(Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_id = Config.API_ID
        self.api_hash = Config.API_HASH
        self.bot_token = Config.BOT_TOKEN
        
    def on_message(self, filters=None, group=-1):
        def decorator(func):
            self.add_handler(MessageHandler(func, filters), group)
            return func

        return decorator

    def on_callback_query(self, filters=None, group=-1):
        def decorator(func):
            self.add_handler(CallbackQueryHandler(func, filters), group)
            return func

        return decorator 
    
    async def start(self):
        await super().start()


class Ubot(Client):
    __module__ = "pyrogram.client"
    _ubot = []
    _prefix = {}
    _get_my_id = []
    _get_my_peer = {}
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_py = PyTgCalls(self)
        self.device_model = "MyYuu"

    def on_message(self, filters=None, group=-1):
        def decorator(func):
            for ub in self._ubot:
               ub.add_handler(MessageHandler(func, filters), group)
            return func

        return decorator

    def pytgcall_close_stream(self):
        def decorator(func):
            for ub in self._ubot:
                ub.call_py.on_update(fl.stream_end)(func)
            return func
        return decorator
        
    @classmethod
    def set_pref(self, user_id, prefix):
        self._prefix[user_id] = prefix

    @classmethod
    async def get_pref(self, user_id):
        return self._prefix.get(user_id, [".", "+", "-", "?", "!"])

    @classmethod
    def cmd_pref(self, cmd):
        command_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")

        async def func(_, client, message):
            if message.text:
                text = message.text.strip().encode("utf-8").decode("utf-8")
                username = client.me.username or ""
                prefixes = await self.get_pref(client.me.id)

                if not text:
                    return False

                for prefix in prefixes:
                    if not text.startswith(prefix):
                        continue

                    without_prefix = text[len(prefix):]

                    for command in cmd.split("|"):
                        if not re.match(
                                rf"^(?:{command}(?:@?{username})?)(?:\s|$)",
                                without_prefix,
                                flags=re.IGNORECASE | re.UNICODE,
                        ):
                            continue

                        without_command = re.sub(
                            rf"{command}(?:@?{username})?\s?",
                            "",
                            without_prefix,
                            count=1,
                            flags=re.IGNORECASE | re.UNICODE,
                        )
                        message.command = [command] + [
                            re.sub(r"\\([\"'])", r"\1", m.group(2) or m.group(3) or "")
                            for m in command_re.finditer(without_command)
                        ]

                        return True

                return False

        return filters.create(func)

    async def start(self):
        await super().start()
        await self.call_py.start()
        handler = await DB.get_prefix(self.me.id)
        self._prefix[self.me.id] = handler if handler else [".", "+", "-", "?", "!"]
        self._get_my_id.append(self.me.id)
        self._ubot.append(self)
        print(f"[MyYuu]:  {self.me.id} Started!!")



TB = Bot(name="bot")
TU = Ubot(name="ubot")


from uu.core.database import *
from uu.core.function import *
from uu.core.helpers import *
