from Bot.Utils.Functions import isValidHexaCode
import discord
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands.core import has_permissions

from sqlalchemy.orm.session import Session
from discord.ext.commands.context import Context
from discord.guild import Guild
from discord.ext.commands.bot import Bot

from Bot.Database.Services.SettingsService import SettingsService
from Bot.Database import session_factory

from discord.embeds import Embed


class GeneralCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    commands.command(
        name="help",
        description="The help command!",
        aliases=["commands", "command"],
        usage="cog",
    )

    @commands.command(name="set_colour",  description="set color descr")
    @has_permissions(administrator=True)
    async def set_colour(self, ctx: Context, str: str = ""):
        if not isValidHexaCode(str):
            return await ctx.send("not valid")

        colour = int(str.replace("#", "0x"), base=16)

        session: Session
        with session_factory() as session:
            service = SettingsService(session)
            settings = service.get_settings(ctx.guild.id)
            settings.colour = colour
            session.commit()

            page = Embed(
                title=settings.get_text_lang("general_color_set_title"),
                description=settings.get_text_lang("general_color_set_description"),
                colour=discord.Colour(colour),
            )
            await ctx.send(embed=page)

    @commands.command(name="ping", description="Ping Pong command")
    async def ping(self, ctx: Context):
        await ctx.send("Pong")


def setup(bot: Bot):
    bot.add_cog(GeneralCog(bot))
