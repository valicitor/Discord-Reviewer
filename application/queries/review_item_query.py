from domain import DataNormalization, Preprocessing, SummarizingData, ExtractingData, AdminItemInsights, GeneralMetadataExtractor, VerificationToken
from config import VERIFICATION_SECRET
from application.handlers.item_review_handler import ItemReviewHandler

class ReviewItemQuery:
  def __init__(self, bot):
    self.bot = bot
    return
  
  async def execute(self, ctx, submission) -> tuple[str, dict | None]:
    if not submission:
        await ctx.send("❌ Error: No submission provided.")
        return "", None

    itemReviewHandler = ItemReviewHandler(self.bot)
    source, results = await itemReviewHandler.handle(ctx, submission)

    adminInsights = AdminItemInsights()
    requires_review, insights = adminInsights.generate(results)
    results['requires_review'] = requires_review
    results['admin_insights'] = insights

    return source, results