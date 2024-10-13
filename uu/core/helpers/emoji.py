from uu import *



class EMO:
    async def PING(client):
        emot_1 = await DB.get_vars(client.me.id, "EMOJI_PING")
        emot_ping = emot_1 if emot_1 else "5415972099766369036"
        if client.me.is_premium:
            _pong = f"<emoji id={emot_ping}>⚡️</emoji>"
        else:
            _pong = ""
        return _pong


    async def MENTION(client):
        emot_2 = await DB.get_vars(client.me.id, "EMOJI_MENTION")
        emot_tion = emot_2 if emot_2 else "5449629507902251736"
        if client.me.is_premium:
            _men = f"<emoji id={emot_tion}>⭐️</emoji>"
        else:
            _men = ""
        return _men


    async def UBOT(client):
        emot_3 = await DB.get_vars(client.me.id, "EMOJI_USERBOT")
        emot_xbot = emot_3 if emot_3 else "4940917565430957022"
        if client.me.is_premium:
            _ubt = f"<emoji id={emot_xbot}>👍</emoji>"
        else:
            _ubt = ""
        return _ubt


    async def PROSES(client):
        emot_4 = await DB.get_vars(client.me.id, "EMOJI_PROSES")
        emot_prs = emot_4 if emot_4 else "5449621648112100255"
        if client.me.is_premium:
            _prses = f"<emoji id={emot_prs}>⭐️</emoji>"
        else:
            _prses = ""
        return _prses


    async def BERHASIL(client):
        emot_5 = await DB.get_vars(client.me.id, "EMOJI_BERHASIL")
        emot_brhsl = emot_5 if emot_5 else "5852871561983299073"
        if client.me.is_premium:
            _berhasil = f"<emoji id={emot_brhsl}>✅</emoji>"
        else:
            _berhasil = ""
        return _berhasil


    async def GAGAL(client):
        emot_6 = await DB.get_vars(client.me.id, "EMOJI_GAGAL")
        emot_ggl = emot_6 if emot_6 else "5852812849780362931"
        if client.me.is_premium:
            _gagal = f"<emoji id={emot_ggl}>❌</emoji>"
        else:
            _gagal = ""
        return _gagal


    async def BROADCAST(client):
        emot_7 = await DB.get_vars(client.me.id, "EMOJI_BROADCAST")
        emot_gcs = emot_7 if emot_7 else "5803175856905917502"
        if client.me.is_premium:
            _bc = f"<emoji id={emot_gcs}>📣</emoji>"
        else:
            _bc = ""
        return _bc


    async def BL_GROUP(client):
        emot_8 = await DB.get_vars(client.me.id, "EMOJI_GROUP")
        emot_gc = emot_8 if emot_8 else "5363943823720333444"
        if client.me.is_premium:
            _grp = f"<emoji id={emot_gc}>⚡️</emoji>"
        else:
            _grp = ""
        return _grp


    async def BL_KETERANGAN(client):
        emot_9 = await DB.get_vars(client.me.id, "EMOJI_KETERANGAN")
        emot_ktrng = emot_9 if emot_9 else "5334882760735598374"
        if client.me.is_premium:
            _ktrn = f"<emoji id={emot_ktrng}>📝</emoji>"
        else:
            _ktrn = ""
        return _ktrn


    async def MENUNGGU(client):
        emot_10 = await DB.get_vars(client.me.id, "EMOJI_MENUNGGU")
        emot_mng = emot_10 if emot_10 else "5413704112220949842"
        if client.me.is_premium:
            _ktr = f"<emoji id={emot_mng}>⏰</emoji>"
        else:
            _ktr = ""
        return _ktr


    async def PUTARAN(client):
        emot_11 = await DB.get_vars(client.me.id, "EMOJI_PUTARAN")
        emot_ptr = emot_11 if emot_11 else "5361600266225326825"
        if client.me.is_premium:
            mmk = f"<emoji id={emot_ptr}>✈️</emoji>"
        else:
            mmk = ""
        return mmk