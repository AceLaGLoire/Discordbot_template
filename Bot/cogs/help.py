import asyncio
from typing import Dict, List
import discord
from discord import message
from discord.embeds import Embed
from discord.ext import commands, tasks
from discord.ext.commands.context import Context
from discord.ext.commands.core import Command

from Bot.Database.Services.SettingsService import SettingsService
from sqlalchemy.orm.session import Session
from Bot.Database import session_factory
from discord.member import Member
from discord.message import Message
from discord.reaction import Reaction
from datetime import datetime


class Help(commands.Cog, name="Help"):
    alive_time_limit = 10  # minutes

    messages: Dict[int, Message] = {}
    reactions = ["🛠️", "🎙️", "📖", "❎", "💅", "🚣", "🧍"]

    def __init__(self, bot):
        self.bot = bot
        self.check_age_task.start()

    def cog_unload(self):
        self.check_age_task.cancel()

    @tasks.loop(seconds=10.0)
    async def check_age_task(self):
        now = datetime.utcnow()
        for id, message in list(self.messages.items()):
            then = message.created_at
            minutes = int((now - then).total_seconds() / 60)
            em = message.embeds[0]
            self.__set_default_footer(
                message.embeds[0], self.alive_time_limit - minutes
            )
            await message.edit(embed=em)

            if minutes >= self.alive_time_limit:
                self.messages.pop(id)
                await message.delete()

    commands.command(
        name="help",
        description="The help command!",
        aliases=["commands", "command"],
        usage="cog",
    )

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: Reaction, user: Member):
        if user.id == self.bot.user.id:
            return

        await reaction.remove(user)

        if not user.id in self.messages.keys():
            return
        # check same channel
        if not reaction.message.channel.id == self.messages[user.id].channel.id:
            return

        prefix = self.__get_prefix(user.guild.id)

        reactionIndex = self.reactions.index(reaction.emoji)
        msg = self.messages[user.id]
        cogs = self.__get_cogs()

        embed = discord.Embed(
            title=f"{self.reactions[reactionIndex]} {cogs[reactionIndex]}",
            description=self.__get_legenda(cogs),
        )

        cog_commands = self.bot.get_cog(f"{cogs[reactionIndex]}").get_commands()
        for comm in cog_commands:
            comm: Command
            description = "_"
            if not comm.description == "":
                description = comm.description

            embed.add_field(
                name=comm, value=f"{description}", inline=True
            )

        now = datetime.utcnow()
        then: datetime = reaction.message.created_at
        minutes = int((now - then).total_seconds() / 60)
        self.__set_default_footer(embed, self.alive_time_limit - minutes)

        await msg.edit(embed=embed)
        self.messages[user.id] = msg

    @commands.command()
    async def help(self, ctx: Context):
        cogs: List[str] = self.__get_cogs()
        prefix: str = self.__get_prefix(ctx.guild.id)

        embed = discord.Embed(
            description=self.__get_legenda(cogs)  # f"Type `{currentPrefix} myprefix` for this server's prefix.\nType `{currentPrefix}setprefix` to change the prefix for this server."
        )

        embed.set_author(
            name=f"{str(self.bot.user).partition('#')[0]}'s Commands and Help",
            icon_url=self.bot.user.avatar_url,
        )
        self.__set_default_footer(embed, self.alive_time_limit)

        for cog in cogs:
            cog_commands = self.bot.get_cog(cog).get_commands()
            commands_list: str = ""
            for comm in cog_commands:
                commands_list += f"`{comm.name}` "
            if not commands_list == "":
                embed.add_field(name=cog, value=commands_list, inline=False)

        msg: Message = await ctx.send(embed=embed)

        for i, _ in enumerate(cogs):
            await msg.add_reaction(self.reactions[i % len(self.reactions)])

        self.messages[ctx.author.id] = msg

    def __get_legenda(self, cogs: List[str]) -> str:
        legenda = ""
        for i, cog in enumerate(cogs):
            legenda += (
                f"Emoij: {self.reactions[i % len(self.reactions)]}  Name: {cog} \n"
            )
        return legenda

    def __get_cogs(self) -> List[str]:
        # hidden_cogs = ["Help", "Functions", "Example Cogs", "Jishaku"]
        return [cog for cog in self.bot.cogs.keys()]

    def __get_prefix(self, guild: int) -> str:
        session: Session
        with session_factory() as session:
            service = SettingsService(session)
            settings = service.get_settings(guild)
            return settings.prefix

    def __set_default_footer(self, embed: Embed, remaining: int):
        embed.set_footer(
            text=f"Help windows time remaing {remaining} minutes.",
            icon_url=self.bot.user.avatar_url,
        )


def setup(bot):
    bot.add_cog(Help(bot))
