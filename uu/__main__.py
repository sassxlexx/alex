import asyncio
from pyrogram import idle
from uu import *


async def start_ubot(ubot_data):
    ubot_ = Ubot(**ubot_data)
    try:
        await asyncio.wait_for(ubot_.start(), timeout=10)
        await ubot_.join_chat("")
        await ubot_.join_chat("")
    except asyncio.TimeoutError:
        pass
    except Exception:
        pass



async def main():
    await TB.start()
    ubots = await DB.get_ubot()
    await asyncio.gather(*(start_ubot(_ubot) for _ubot in ubots))
    await bash("rm -rf *session*")
    await asyncio.gather(loadPlugins(), installPeer(), exp_ubot())
    await asyncio.Event().wait()


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())
