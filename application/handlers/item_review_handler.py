from domain import SummarizingData, Preprocessing, ClusterManager

class ItemReviewHandler:

    def __init__(self, bot):
        self.bot = bot
        self.cluster_manager = ClusterManager(self.bot)
    
    async def handle(self, ctx, submission) -> tuple[str, list[str] | None]:
        if not submission:
            return None
        
        source, token, item_data = await self.cluster_manager.extract_and_cluster(ctx, submission)
        description_fields = await self.cluster_manager.find_fields(item_data, ["item description", "item effects", "extra information"])
        description_text = self.get_content(description_fields)

        summary_fields = await self.cluster_manager.find_fields(item_data, ["item description"])
        effects_fields = await self.cluster_manager.find_fields(item_data, ["item effects"])

        word_count = len(description_text.split())
        summarizer = SummarizingData()

        bullet_count = min(max(word_count // 75, 3), 8)

        prep = Preprocessing()
        processed = prep.preprocess(description_text)
        agg_processed_sents = prep.aggressive_pass(processed)

        name_value = await self.extract_field(item_data, "name")
        itype_value = await self.extract_field(item_data, "type")
        rank_value = await self.extract_field(item_data, "tier")
        assistant_value = await self.extract_field(item_data, "assistant")
        cooldown_value = await self.extract_field(item_data, "cooldown")
        ki_value = await self.extract_field(item_data, "ki type")
        artificialpl_value = await self.extract_field(item_data, "artificial pl")

        results = {
            "requires_review": False,
            "admin_insights": [],
            "item_name": [name_value],
            "type": [itype_value],
            "rank": [rank_value],
            "cooldown": [cooldown_value],
            "assistant": [assistant_value],
            "ki": [ki_value],
            "artificialpl": [artificialpl_value],
            "summary": summarizer.summarize_text(self.get_content(summary_fields), 4),
            "effects": summarizer.summarize_text(self.get_content(effects_fields), 4),
            "bullet_points": summarizer.summarize_bullet_points(agg_processed_sents, bullet_count),
            "verification_token": token
        }
        return source, results
    
    def get_content(self, fields: list[str]) -> str:
        if not fields:
            return ""
        else:
            return " ".join(fields) if fields else ""
    
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