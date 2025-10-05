import discord
from discord.ext import commands
import asyncio
from domain import DiscordEmbed
from domain import VerificationToken, DataNormalization, Preprocessing, SummarizingData, ExtractingData, CategoryEvaluator, PowerAnalyzer, AdminAbilityInsights, GeneralMetadataExtractor, MessyTextDataExtractor, ClusterManager
from infrastructure import CategoryRepository
from config import VERIFICATION_SECRET


class TestCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="test_clustering")
    @commands.has_permissions(administrator=True)
    async def test_clustering(self, ctx, *, submission):
        testComponent = ClusterManager(self.bot)

        output = str(await testComponent.extract_and_cluster(ctx, submission))
        print(output)
        await ctx.send(f"Output:\n{output[:1980]}...")

    @commands.command(name="test_data_finding")
    @commands.has_permissions(administrator=True)
    async def test_data_finding(self, ctx, field: str, *, submission):
        testComponent = ClusterManager(self.bot)

        clusters = await testComponent.extract_and_cluster(ctx, submission)

        output = str(await testComponent.find_fields(clusters, [field]))
        await ctx.send(f"Output:\n{output[:1980]}...")

    @commands.command(name="test_finding_multi_data")
    @commands.has_permissions(administrator=True)
    async def test_finding_multi_data(self, ctx, field_1: str, field_2: str, field_3: str, *, submission):
        testComponent = ClusterManager(self.bot)

        print("Extracting and clustering...")
        clusters = await testComponent.extract_and_cluster(ctx, submission)

        print(f"Finding fields... {field_1}, {field_2}, {field_3}")
        fields = await testComponent.find_fields(clusters, [field_1, field_2, field_3])

        print("Fields found...")
        output = str(fields)
        await ctx.send(f"Output:\n{output[:1980]}...")

    @commands.command(name="test_summarizer")
    @commands.has_permissions(administrator=True)
    async def test_summarizer(self, ctx, field: str, *, submission):
        testComponent = ClusterManager(self.bot)

        clusters = await testComponent.extract_and_cluster(ctx, submission)
        found_data = await testComponent.find_fields(clusters, [field])

        output = ""
        if found_data:
            processed_text = " ".join(found_data) if found_data else ""

            # Summarize the submission
            word_count = len(processed_text.split())
            summarizer = SummarizingData()

            summary_sent_count = min(max(word_count // 75, 4), 10)
            output = summarizer.summarize_text(processed_text,
                                               summary_sent_count)

        await ctx.send(f"Output:\n{output[:1980]}...")

    @commands.command(name="test_bulletpoints")
    @commands.has_permissions(administrator=True)
    async def test_bulletpoints(self, ctx, field: str, *, submission):
        testComponent = ClusterManager(self.bot)

        clusters = await testComponent.extract_and_cluster(ctx, submission)
        found_data = await testComponent.find_fields(clusters, [field])

        output = ""
        if found_data:
            processed_text = " ".join(found_data) if found_data else ""

            # Summarize the submission
            word_count = len(processed_text.split())
            bullet_count = min(max(word_count // 75, 3), 8)
            summarizer = SummarizingData()
            prep = Preprocessing()

            processed = prep.preprocess(processed_text)
            agg_processed_sents = prep.aggressive_pass(processed)
            bullet_points = summarizer.summarize_bullet_points(
                agg_processed_sents, bullet_count)
            output = "\n".join(bullet_points)

        await ctx.send(f"Output:\n{output[:1980]}...")

    @commands.command(name="test_category_assignment")
    @commands.has_permissions(administrator=True)
    async def test_category_assignment(self, ctx, field: str, *, submission):
        testComponent = ClusterManager(self.bot)

        clusters = await testComponent.extract_and_cluster(ctx, submission)
        found_data = await testComponent.find_fields(clusters, [field])

        output = ""
        if found_data:
            processed_text = " ".join(found_data) if found_data else ""
            repository = CategoryRepository()
            categories = await repository.get_all(ctx.guild.id)
            categoryEvaluator = CategoryEvaluator(categories)
            top_categories = categoryEvaluator.evaluate(processed_text)
            output = str(top_categories)

        await ctx.send(f"Output:\n{output[:1980]}...")
    
    @commands.command(name="test_category_compare")
    @commands.has_permissions(administrator=True)
    async def test_category_compare(self, ctx, top_category: str, *, expected_category: str):
        adminAbilityInsights = AdminAbilityInsights()
        output = adminAbilityInsights.compare_categories([top_category], expected_category)

        await ctx.send(f"Output:\n{output}...")

    @commands.command(name="test_power_analyzer")
    @commands.has_permissions(administrator=True)
    async def test_power_analyzer(self, ctx, field: str, *, submission):
        testComponent = ClusterManager(self.bot)

        clusters = await testComponent.extract_and_cluster(ctx, submission)
        found_data = await testComponent.find_fields(clusters, [field])

        output = ""
        if found_data:
            processed_text = " ".join(found_data) if found_data else ""

            analyzer = PowerAnalyzer()
            power_scores = analyzer.analyze(processed_text)

            output = str(power_scores)

        await ctx.send(f"Output:\n{output[:1980]}...")

    @commands.command(name="test_long_task")
    @commands.has_permissions(administrator=True)
    async def test_long_task(self, ctx):
        # Step 1: send placeholder embed
        embed = discord.Embed(
            title="Processing...",
            description="Please wait ⏳",
            color=discord.Color.orange()
        )
        msg = await ctx.send(embed=embed)

        # Step 2: simulate long task
        await asyncio.sleep(5)

        # Step 3: edit embed with results
        result_embed = discord.Embed(
            title="Done!",
            description="Here are the results ✅",
            color=discord.Color.green()
        )
        await msg.edit(embed=result_embed)

async def setup(bot):
    await bot.add_cog(TestCog(bot))
