from pyrogram import Client
from dotenv import dotenv_values
import logging
from importlib import import_module
from os import listdir

CONFIG = dotenv_values("config.env")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(message)s",
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()],
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

MUST_REQUIRED_KEYS = ["API_ID", "API_HASH", "BOT_TOKEN"]
for key in MUST_REQUIRED_KEYS:
    if key not in CONFIG:
        raise Exception(f"{key} is missing in config.env")


class Bot(Client):
    def __init__(self):
        super().__init__(
            "bot",
            api_id=CONFIG["API_ID"],
            api_hash=CONFIG["API_HASH"],
            bot_token=CONFIG["BOT_TOKEN"],
            sleep_threshold=30,
        )

    async def start(self):
        global BOT_INFO
        await super().start()
        BOT_INFO = await self.get_me()
        LOGGER.info(f"Bot Started As {BOT_INFO.username}\n")

    def load_plugins(self):
        for file in listdir("bot/plugins"):
            if file.endswith(".py"):
                try:
                    import_module("bot.plugins." + file[:-3])
                    LOGGER.info(f"Loaded {file}")
                except Exception as e:
                    LOGGER.error(f"{file} failed to load.\n{e}")

    async def stop(self, *args):
        await super().stop()
        LOGGER.info("Bot Stopped, Bye.")


bot = Bot()
