from Bot.Utils.Constance import COG_PATH
import discord
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context


class AdminCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(help="Loads an extension. Bot Owner only!")
    @commands.is_owner()
    async def load(self, ctx: Context, extension_name: str):
        try:
            self.bot.load_extension(COG_PATH.replace("/", ".") + extension_name)
        except (AttributeError, ImportError) as e:
            await ctx.send(f"```py\n{type(e).__name__}: {str(e)}\n```")
            return

        await ctx.send(f"{extension_name} loaded.")

    @commands.command(help="Unloads an extension. Bot Owner only!")
    @commands.is_owner()
    async def unload(self, ctx: Context, extension_name: str):
        self.bot.unload_extension(COG_PATH.replace("/", ".") + extension_name)
        await ctx.send(f"{extension_name} unloaded.")


def setup(bot: Bot):
    bot.add_cog(AdminCog(bot))
