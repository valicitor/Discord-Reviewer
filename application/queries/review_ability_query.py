from domain import  AdminAbilityInsights
from application.handlers.ability_review_handler import AbilityReviewHandler

class ReviewAbilityQuery:

    def __init__(self, bot):
        self.bot = bot
        return

    async def execute(self, ctx, submission) -> tuple[str, dict | None]:
        if not submission:
            await ctx.send("❌ Error: No submission provided.")
            return "", None

        abilityReviewHandler = AbilityReviewHandler(self.bot)
        source, results = await abilityReviewHandler.handle(ctx, submission)

        adminInsights = AdminAbilityInsights()
        requires_review, insights = adminInsights.generate(results)
        results['requires_review'] = requires_review
        results['admin_insights'] = insights

        return source, results