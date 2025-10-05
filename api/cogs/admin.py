from discord.ext import commands
from domain import DiscordEmbed
from application import UpsertPrefixCommand, VerifyContentQuery


class AdminCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="set_prefix")
    @commands.has_permissions(administrator=True)
    async def set_prefix(self, ctx, new_prefix: str):

        query = UpsertPrefixCommand(ctx.guild.id, new_prefix)
        result = await query.execute()

        if not result:
            await ctx.send("❌ Failed to update prefix. Please try again.")

        await ctx.send(embed=DiscordEmbed.prefix_changed_embed(ctx,
            new_prefix, ctx.author.name))

    @commands.command(name="verify_content", aliases=['verify'])
    @commands.has_permissions(administrator=True)
    async def verify_content(self, ctx, hash, submission):

        query = VerifyContentQuery(self.bot)
        result = await query.execute(ctx, hash, submission)

        await ctx.send(
            embed=DiscordEmbed.submission_verified_embed(ctx, result))

    @commands.command(name="approved")
    @commands.has_permissions(administrator=True)
    async def approved(self, ctx):
        await ctx.send(embed=DiscordEmbed.approved_embed(ctx))

    @commands.command(name="denied")
    @commands.has_permissions(administrator=True)
    async def denied(self, ctx):
        await ctx.send(embed=DiscordEmbed.denied_embed(ctx))

    @commands.command(name="real_teapot")
    @commands.has_permissions(administrator=True)
    async def real_teapot(self, ctx):
        await ctx.send(embed=DiscordEmbed.real_teapot_embed(ctx))

    @commands.command(name="father_koko")
    @commands.has_permissions(administrator=True)
    async def father_koko(self, ctx):
        await ctx.send(embed=DiscordEmbed.fatherkoko_embed(ctx))

    @commands.command(name="star_light")
    @commands.has_permissions(administrator=True)
    async def star_light(self, ctx):
        await ctx.send(embed=DiscordEmbed.starlight_embed(ctx))


async def setup(bot):
    await bot.add_cog(AdminCog(bot))
