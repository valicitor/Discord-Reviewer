from domain import DataNormalization, ExtractingData, TrainingLogEvaluator
from application.handlers.training_review_handler import TrainingReviewHandler

class ReviewTrainingQuery:
  def __init__(self, bot):
    self.bot = bot
    return
  
  async def execute(self, ctx, submission) -> tuple[str, dict | None]:
    if not submission:
      await ctx.send("❌ Error: No submission provided.")
      return "", None

    # Extract content from the submission if it contains a URL
    trainingReviewHandler = TrainingReviewHandler(self.bot)
    source, results = await trainingReviewHandler.handle(ctx, submission)

    return source, results