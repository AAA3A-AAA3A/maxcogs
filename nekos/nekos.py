import aiohttp
import discord
from redbot.core import commands

NEKOS_API = "https://nekos.best/"


class Nekos(commands.Cog):
    """Sending nekos images from nekos.best."""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())

    __version__ = "0.6.0"
    __author__ = "MAX"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthor: {self.__author__}\nCog Version: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    @commands.command(aliases=["nekos"])
    @commands.cooldown(1, 3, commands.BucketType.guild)
    @commands.max_concurrency(1, commands.BucketType.guild)
    @commands.bot_has_permissions(embed_links=True)
    async def neko(self, ctx):
        """Send a random neko image."""
        async with aiohttp.ClientSession() as session:
            async with session.get(NEKOS_API + "nekos") as response:
                if response.status != 200:
                    return await ctx.send(
                        "Something went wrong while trying to contact API."
                    )
                url = await response.json()
            emb = discord.Embed(title="Here's a pic of neko")
            emb.colour = await ctx.embed_color()
            emb.set_footer(text="Powered by nekos.best")
            emb.set_image(url=url["url"])
        try:
            await ctx.send(embed=emb)
        except discord.HTTPException:
            await ctx.send("Something went wrong while posting an image.")
