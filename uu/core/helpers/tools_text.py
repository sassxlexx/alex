from uu import *

class MSG:     
    def START(message):
        return f"""
<b>👋🏻 Hallo <a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>!
@{TB.me.username} userbot yang bisa kalian buat dengan mudah.</b>
"""
    async def UBOT(count):
        return f"""
<b>Userbot Ke</b> <code>{int(count) + 1}/{len(TU._ubot)}</code>
<b>Akun:</b> <a href=tg://user?id={TU._ubot[int(count)].me.id}>{TU._ubot[int(count)].me.first_name} {TU._ubot[int(count)].me.last_name or ''}</a> 
<b>ID:</b> <code>{TU._ubot[int(count)].me.id}</code>
<b>Nomer Telpon:</b> <code>{TU._ubot[int(count)].me.phone_number}</code>
"""
