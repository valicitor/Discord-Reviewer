from discord.ext import commands
from domain import DiscordEmbed
from application import CreateCategoryCommand, DeleteCategoryCommand, DeleteAllCategoriesCommand, ViewAllCategoriesQuery, ViewCategoryQuery

class CategoriesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='create_category', aliases=['create'])
    @commands.has_permissions(administrator=True)
    async def create_category(self, ctx, category_name: str, priority: int, *, prompt: str):

        command = CreateCategoryCommand(ctx.guild.id, category_name, priority, prompt)
        result = await command.execute()

        if not result:
            return await ctx.send(embed=DiscordEmbed.create_category_embed(None))

        query = ViewCategoryQuery(ctx.guild.id, category_name)
        category = await query.execute()

        await ctx.send(embed=DiscordEmbed.create_category_embed(category))

    @commands.command(name='delete_category', aliases=['delete'])
    @commands.has_permissions(administrator=True)
    async def delete_category(self, ctx, category_name: str):

        query = ViewCategoryQuery(ctx.guild.id, category_name)
        category = await query.execute()

        command = DeleteCategoryCommand(ctx.guild.id, category_name)
        result = await command.execute()

        await ctx.send(embed=DiscordEmbed.delete_category_embed(category))

    @commands.command(name='delete_all_categories', aliases=['delete_all'])
    @commands.has_permissions(administrator=True)
    async def delete_all_categories(self, ctx):
        
        command = DeleteAllCategoriesCommand(ctx.guild.id)
        result = await command.execute()

        await ctx.send(embed=DiscordEmbed.delete_all_categories_embed(result))

    @commands.command(name='view_category', aliases=['view'])
    @commands.has_permissions(administrator=True)
    async def view_category(self, ctx, category_name: str):
        
        query = ViewCategoryQuery(ctx.guild.id, category_name)
        category = await query.execute()

        await ctx.send(embed=DiscordEmbed.view_category_embed(category))

    @commands.command(name='view_all_categories', aliases=['view_all'])
    @commands.has_permissions(administrator=True)
    async def view_all_categories(self, ctx):

        query = ViewAllCategoriesQuery(ctx.guild.id)
        categories = await query.execute()
        
        await ctx.send(embed=DiscordEmbed.view_all_categories_embed(categories))

async def setup(bot):
  await bot.add_cog(CategoriesCog(bot))