from Bot.Utils.Constance import COG_PATH
from Bot.Database.Services.SettingsService import SettingsService
from sqlalchemy.orm.session import Session
from Bot.Database import session_factory
from discord.ext.commands.context import Context
from Bot.Utils.Functions import log
from discord.message import Message
from discord.flags import Intents

import glob

import os, discord, logging
from discord.ext import commands
from discord.ext.commands.bot import Bot

# logging
if os.getenv("ENV") == "development":
    logger = logging.getLogger("discord")
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
    handler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )
    logger.addHandler(handler)


async def determine_prefix(bot, message: Message):
    session: Session
    with session_factory() as session:
        service = SettingsService(session)
        item = service.get_settings(message.guild.id)
    return item.prefix


intents: Intents = discord.Intents.default()
intents.members = True
intents.typing = False
bot: Bot = commands.Bot(
    intents=intents, command_prefix=determine_prefix, case_insensitive=True
)
bot.remove_command("help")

for cog_name in glob.glob(COG_PATH + "*.py"):
    cog_name = cog_name.replace(COG_PATH, "").replace(".py", "")
    bot_path = COG_PATH.replace("/", ".")
    bot.load_extension(bot_path + cog_name)


def run_bot():
    bot.run(os.getenv("TOKEN"))
