from discord.ext import commands
from domain import DiscordEmbed
from application import GetPrefixQuery

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', aliases=['h'])
    async def help(self, ctx, *, command_name=None):
        query = GetPrefixQuery(ctx.guild.id)
        prefix = await query.execute()

        if not command_name:
            await ctx.send(embed=DiscordEmbed.help_embed(prefix))  
        else:
            command = self.bot.get_command(command_name.lower())
            if not command:
                await ctx.send(embed=DiscordEmbed.command_not_found(command_name))
            else:
                await ctx.send(embed=DiscordEmbed.command_help(command, prefix))
    
    @commands.command(name='faq')
    async def faq(self, ctx):
        query = GetPrefixQuery(ctx.guild.id)
        prefix = await query.execute()
    
        await ctx.send(embed=DiscordEmbed.command_faq(prefix))


async def setup(bot):
    await bot.add_cog(HelpCog(bot))
