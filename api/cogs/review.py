import discord
from discord.ext import commands
from domain import DiscordEmbed
from application import ReviewCharacterQuery, ReviewAbilityQuery, ReviewItemQuery, ReviewTrainingQuery


class AbilityReviewButton(discord.ui.Button):
    def __init__(self, ability: dict):
        super().__init__(
            label=f"Review {ability.get("name") or "Unknown"}",
            style=discord.ButtonStyle.primary
        )
        self.ability = ability

    async def callback(self, interaction: discord.Interaction):
        # Defer interaction (thinking)
        await interaction.response.defer(thinking=True)

        # Build submission text
        submission_text = "\n".join(f"{k}: {v}" for k, v in self.ability.items())

        # Run your review logic
        query = ReviewAbilityQuery(interaction.client)
        source_type, results = await query.execute(interaction, submission_text)

        # Make sure your embed is a proper discord.Embed object
        embed = DiscordEmbed.review_ability_embed(interaction, source_type, interaction.user.display_name, results)
        if not isinstance(embed, discord.Embed):
            embed = discord.Embed(
                title="Error",
                description="Failed to generate embed.",
                color=discord.Color.red()
            )

        # Send follow-up
        await interaction.followup.send(embed=embed)

class AbilityReviewView(discord.ui.View):
    def __init__(self, abilities: list[dict]):
        super().__init__(timeout=None)  # persistent until stopped
        for ability in abilities:
            name = ability.get("name") or "Unknown"
            self.add_item(AbilityReviewButton(ability))

class ReviewCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='review_character', aliases=['rchar'])
    @commands.has_permissions(administrator=True)
    async def review_character(self, ctx, *, submission):

        query = ReviewCharacterQuery(self.bot)
        source_type, results, abilities = await query.execute(ctx, submission)

        view = AbilityReviewView(abilities)
    
        await ctx.send(embed=DiscordEmbed.review_character_embed(ctx, source_type, results), view=view)
      
    @commands.command(name='review_item', aliases=['ritem'])
    @commands.has_permissions(administrator=True)
    async def review_item(self, ctx, *, submission):

        query = ReviewItemQuery(self.bot)
        source_type, results = await query.execute(ctx, submission)
    
        await ctx.send(embed=DiscordEmbed.review_item_embed(ctx, source_type, results))
      
    @commands.command(name='review_ability', aliases=['rability'])
    @commands.has_permissions(administrator=True)
    async def review_ability(self, ctx, *, submission):

        query = ReviewAbilityQuery(self.bot)
        source_type, results = await query.execute(ctx, submission)
        
        await ctx.send(embed=DiscordEmbed.review_ability_embed(ctx, source_type, ctx.author.display_name, results))  
        
    @commands.command(name='review_training', aliases=['rtraining'])
    @commands.has_permissions(administrator=True)
    async def review_training(self, ctx, *, submission):

        query = ReviewTrainingQuery(self.bot)
        source_type, results = await query.execute(ctx, submission)

        # await ctx.send(f"{results['content']}")
        await ctx.send(embed=DiscordEmbed.review_training_log_embed(ctx, source_type, results))  

async def setup(bot):
  await bot.add_cog(ReviewCog(bot))