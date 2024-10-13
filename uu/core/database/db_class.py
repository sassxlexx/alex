import sys

from motor.motor_asyncio import AsyncIOMotorClient
from config import Config



class Database(object):
    def __init__(self):
        self.client = AsyncIOMotorClient(Config.MONGO_URL)
        self.db = self.client["MyYuuUbotDB"]

        # mongo db collections
        self.ubotdb = self.db.ubotdb
        self.prefixes = self.db.prefixes
        self.varsdb = self.db.varsdb
        self.expU = self.db.expU
        self.pm_pr = self.db.pm_pr


    async def set_warn_limit(self, user_id, limit):
        await DB.set_vars(user_id, f"limit_warn", limit)

    async def get_warn_limit(self, user_id):
        limit = await DB.get_vars(user_id, f"limit_warn")
        return limit if limit else 3

    async def set_action(self, user_id, value):
        await DB.set_vars(user_id, f"action_warn", value)

    async def get_action(self, user_id):
        action_type = await DB.get_vars(user_id, f"action_warn")
        return action_type if action_type else "mute"

    async def get_warn(self, user_id):
        warnings = await DB.get_vars(user_id, "warnings")
        return warnings if warnings else 0

    async def add_warn(self, user_id):
        current_warnings = await DB.get_warn(user_id)
        new_warnings = current_warnings + 1
        await DB.set_vars(user_id, "warnings", new_warnings)
        return new_warnings

    async def reset_warn(self, user_id):
        await DB.remove_vars(user_id, "warnings")

    
    # PM PERMIT
    async def approve_pm(self, user_id: int) -> bool:
        users = await self.get_pm()
        users.append(user_id)
        await self.pm_pr.update_one(
            {"pm": "pm"}, {"$set": {"user_ids": users}}, upsert=True
        )
        return True

    async def disapprove_pm(self, user_id: int) -> bool:
        users = await self.get_pm()
        users.remove(user_id)
        await self.pm_pr.update_one(
            {"pm": "pm"}, {"$set": {"user_ids": users}}, upsert=True
        )
        return True

    async def get_pm(self) -> list:
        users = await self.pm_pr.find_one({"pm": "pm"})
        if not users:
            return []
        return users["user_ids"]
    
    # USERBOT
    async def add_ubot(self, user_id, api_id, api_hash, session_string):
        return await self.ubotdb.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "api_id": api_id,
                    "api_hash": api_hash,
                    "session_string": session_string,
                }
            },
            upsert=True,
        )


    async def remove_ubot(self, user_id):
        return await self.ubotdb.delete_one({"user_id": user_id})


    async def get_ubot(self):
        data = []
        async for ubot in self.ubotdb.find({"user_id": {"$exists": 1}}):
            data.append(
                dict(
                    name=str(ubot["user_id"]),
                    api_id=ubot["api_id"],
                    api_hash=ubot["api_hash"],
                    session_string=ubot["session_string"],
                )
            )
        return data

    # PREFIX
    async def get_prefix(self, user_id):
        hndlr = [".", "+", "-", "?", "!"]
        sh = await self.prefixes.find_one({"_id": user_id})
        if sh:
            return sh.get("prefixesi")
        else:
            return hndlr

    async def set_prefix(self, user_id, prefix):
        await self.prefixes.update_one(
            {"_id": user_id}, {"$set": {"prefixesi": prefix}}, upsert=True
        )

    async def remove_prefix(self, user_id):
        await self.prefixes.update_one(
            {"_id": user_id}, {"$unset": {"prefixesi": ""}}, upsert=True
        )


    # EXP UBOT
    async def get_expired(self, user_id):
        user = await self.expU.find_one({"_id": user_id})
        if user:
            return user.get("expire_date")
        else:
            return None


    async def set_expired(self, user_id, expire_date):
        await self.expU.update_one(
            {"_id": user_id}, {"$set": {"expire_date": expire_date}}, upsert=True
        )


    async def remove_expired(self, user_id):
        await self.expU.update_one(
            {"_id": user_id}, {"$unset": {"expire_date": ""}}, upsert=True
        )


    # VARS
    async def set_vars(self, user_id, vars_name, value, query="vars"):
        update_data = {"$set": {f"{query}.{vars_name}": value}}
        await self.varsdb.update_one({"_id": user_id}, update_data, upsert=True)

    async def get_vars(self, user_id, vars_name, query="vars"):
        result = await self.varsdb.find_one({"_id": user_id})
        return result.get(query, {}).get(vars_name, None) if result else None

    async def remove_vars(self, user_id, vars_name, query="vars"):
        remove_data = {"$unset": {f"{query}.{vars_name}": ""}}
        await self.varsdb.update_one({"_id": user_id}, remove_data)

    async def all_vars(self, user_id, query="vars"):
        result = await self.varsdb.find_one({"_id": user_id})
        return result.get(query) if result else None

    async def remove_all_vars(self, user_id):
        await self.varsdb.delete_one({"_id": user_id})

    async def get_list_vars(self, user_id, vars_name, query="vars"):
        vars_data = await DB.get_vars(user_id, vars_name, query)
        return [int(x) for x in str(vars_data).split()] if vars_data else []

    async def add_list_vars(self, user_id, vars_name, value, query="vars"):
        vars_list = await DB.get_list_vars(user_id, vars_name, query)
        vars_list.append(value)
        await DB.set_vars(user_id, vars_name, " ".join(map(str, vars_list)), query)

    async def remove_list_vars(self, user_id, vars_name, value, query="vars"):
        vars_list = await DB.get_list_vars(user_id, vars_name, query)
        if value in vars_list:
            vars_list.remove(value)
            await DB.set_vars(user_id, vars_name, " ".join(map(str, vars_list)), query)


DB = Database()
