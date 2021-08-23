import discord
from discord.ext import commands
from discord.ext.commands.bot import Bot
from sqlalchemy.orm.session import Session

from discord.guild import Guild
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context

from Bot.Database.Services.SettingsService import SettingsService
from Bot.Database import session_factory


class EventsCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command(self, ctx: Context):
        session: Session
        with session_factory() as session:
            service = SettingsService(session)
            settings = service.get_settings(ctx.guild.id)
            if settings.delete_command_message:
                try:
                    await ctx.message.delete()
                except Exception as e:
                    print(f"{e}")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: Guild):
        session: Session
        with session_factory() as session:
            service = SettingsService(session)
            service.create_if_not_exists(guild.id)
            session.close()

    @commands.Cog.listener()
    async def on_ready(self):
        session: Session
        with session_factory() as session:
            guild: Guild
            for guild in self.bot.guilds:
                service = SettingsService(session)
                service.create_if_not_exists(guild.id)
            session.close()


def setup(bot: Bot):
    bot.add_cog(EventsCog(bot))
