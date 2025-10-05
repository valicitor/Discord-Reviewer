from domain import ClusterManager, TrainingLogEvaluator

class TrainingReviewHandler:

    def __init__(self, bot):
        self.bot = bot
        self.cluster_manager = ClusterManager(self.bot)
    
    async def handle(self, ctx, submission) -> tuple[str, list[str] | None]:
        if not submission:
            return None
        
        source, token, training_data = await self.cluster_manager.extract_and_cluster(ctx, submission)
        if not training_data:
            return source, None
        
        trainingLogEvaluator = TrainingLogEvaluator()
        eval_results = trainingLogEvaluator.evaluate(training_data)

        results = {
            "requires_review": False,
            "admin_insights": [],
            "total_correct": eval_results.get('total_correct', ''),
            "total_entries": eval_results.get('total_entries', ''),
            "bad_entries": eval_results.get('bad_entries', '')
        }

        return source, results