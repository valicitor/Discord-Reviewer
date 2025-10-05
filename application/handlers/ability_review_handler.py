from domain import SummarizingData, Preprocessing, CategoryEvaluator, PowerAnalyzer, ClusterManager
from infrastructure import CategoryRepository

class AbilityReviewHandler:

    def __init__(self, bot):
        self.bot = bot
        self.cluster_manager = ClusterManager(self.bot)
    
    async def handle(self, ctx, submission) -> tuple[str, list[str] | None]:
        if not submission:
            return None
        
        source, token, ability_data = await self.cluster_manager.extract_and_cluster(ctx, submission)
        description_fields = await self.cluster_manager.find_fields(ability_data, ["description", "extra effects", "consequences"])
        description_text = ""
        if not description_fields:
            # No description found
            description_text = submission
        else:
            description_text = " ".join(description_fields) if description_fields else ""

        word_count = len(description_text.split())
        summarizer = SummarizingData()

        summary_sent_count = min(max(word_count // 75, 4), 10)
        bullet_count = min(max(word_count // 75, 3), 8)

        prep = Preprocessing()
        processed = prep.preprocess(description_text)
        agg_processed_sents = prep.aggressive_pass(processed)


        name_value = await self.extract_field(ability_data, "name")
        atype_value = await self.extract_field(ability_data, "ability type")
        multiplier_value = await self.extract_field(ability_data, "multiplier")

        rank = await self.extract_field(ability_data, "tier")
        cooldown = await self.extract_field(ability_data, "cooldown")

        # Check if extraction looks valid
        def is_valid(value, field_name):
            if not value:
                return False
            # crude check: rank should contain "Tier", cooldown should contain a number
            if field_name == "tier":
                return "Tier" in value
            elif field_name == "cooldown":
                return any(char.isdigit() for char in value)
            return True

        if not is_valid(rank, "tier") or not is_valid(cooldown, "cooldown"):
            # fallback to combined parsing
            combined_str = await self.get_field_value(ability_data, "cooldown")
            if combined_str:
                parsed_rank, parsed_cooldown = await self.rank_cooldown_splitter(combined_str)
                rank = parsed_rank
                cooldown = parsed_cooldown

        repository = CategoryRepository()
        categories = await repository.get_all(ctx.guild.id)
        categoryEvaluator = CategoryEvaluator(categories)
        top_categories = categoryEvaluator.evaluate(description_text)

        analyzer = PowerAnalyzer()
        power_scores = analyzer.analyze(description_text)

        result = {
            "requires_review": False,
            "admin_insights": [],
            "ability_name": [name_value],
            "ability_type": [atype_value],
            "multiplier": [multiplier_value],
            "cooldown": [cooldown],
            "rank": [rank],
            "top_categories": top_categories,
            "summary": summarizer.summarize_text(description_text, summary_sent_count),
            "bullet_points": summarizer.summarize_bullet_points(agg_processed_sents, bullet_count),
            "power_scores": power_scores,
            "verification_token": token
        }
        return source, result
    
    async def extract_field(self, data, field_name: str) -> str:
        field_str = await self.get_field_value(data, field_name)
        if field_str and field_name.lower() in field_str.lower():
            # Header is still present, split it
            _, value = await self.split_header_value(field_str)
            return value
        return field_str
    
    async def get_field_value(self, data, field_name: str) -> str | None:
        found_fields = await self.cluster_manager.find_fields(data, [field_name])
        if found_fields:
            return " ".join(found_fields)
        return None

    async def split_header_value(self, text: str) -> tuple[str, str]:
        if not text:
            return None, ""

        parts = text.split(" ", 1)
        if len(parts) == 2:
            return parts[0], parts[1]
        
        # Fallback: only header, no value
        return None, text

    async def rank_cooldown_splitter(self, text: str) -> tuple[str | None, str | None]:
        # Match [RANK] at the start
        parts = [part for part in text.split('  ')]
        if len(parts) == 2:
            rank, cooldown = parts
        else:
            # Fallback if marker not present
            rank = parts[0]
            cooldown = None

        return rank, cooldown