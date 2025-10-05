from domain import AdminCharacterInsights
from application.handlers.character_review_handler import CharacterReviewHandler

class ReviewCharacterQuery:
  def __init__(self, bot):
    self.bot = bot
    return
  
  async def execute(self, ctx, submission) -> tuple[str, dict | None, list[dict] | None]:
    if not submission:
        await ctx.send("❌ Error: No submission provided.")
        return "", None

    characterReviewHandler = CharacterReviewHandler(self.bot)
    source, results, abilities = await characterReviewHandler.handle(ctx, submission)

    adminInsights = AdminCharacterInsights()
    requires_review, insights = adminInsights.generate(results)
    results['requires_review'] = requires_review
    results['admin_insights'] = insights

    return source, results, abilities
