import os

from pyrogram import filters

class Config(object):
    MAX_BOT = int(os.getenv("MAX_BOT", "9999"))
    API_ID = int(os.getenv("API_ID", "26190940"))
    API_HASH = os.getenv("API_HASH", "bb831f9e337b4c53f0faf8da0e1de8bd")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "5614304376:AAE9lICgMbLPBzSPQUW7k1p0Z1VVRFQa1bk")
    OWNER_ID = int(os.getenv("OWNER_ID", "5574927008"))
    GROUP_SELLER = int(os.getenv("GROUP_SELLER", "-1002191896661"))
    RMBG_API = os.getenv("RMBG_API", "a6qxsmMJ3CsNo7HyxuKGsP1o")
    MONGO_URL = os.getenv(
        "MONGO_URL",
        "mongodb+srv://pribadilexcz666:pribadilexcz666@cluster0.s1qba.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    )
    OPENAI_KEY = os.getenv(
    "OPENAI_KEY",
    "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",
    )