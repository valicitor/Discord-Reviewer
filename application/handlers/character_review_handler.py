from domain import SummarizingData, Preprocessing, ClusterManager

class CharacterReviewHandler:

    def __init__(self, bot):
        self.bot = bot
        self.cluster_manager = ClusterManager(self.bot)
    
    async def handle(self, ctx, submission) -> tuple[str, list[str] | None, list[dict] | None]:
        if not submission:
            return None
        
        source, token, character_data = await self.cluster_manager.extract_and_cluster(ctx, submission)
        character_data, starting_abilities = await self.cluster_manager.extract_starting_abilities(character_data)

        description_fields = await self.cluster_manager.find_fields(character_data, ["character summary", "physical description", "perceived personality", "backstory"])
        description_text = self.get_content(description_fields)

        summary_fields = await self.cluster_manager.find_fields(character_data, ["character summary"])
        physcial_fields = await self.cluster_manager.find_fields(character_data, ["physical description"])
        personality_fields = await self.cluster_manager.find_fields(character_data, ["perceived personality"])
        backstory_fields = await self.cluster_manager.find_fields(character_data, ["backstory"])

        word_count = len(description_text.split())
        summarizer = SummarizingData()

        bullet_count = min(max(word_count // 75, 3), 8)

        prep = Preprocessing()
        processed = prep.preprocess(description_text)
        agg_processed_sents = prep.aggressive_pass(processed)

        name_value = await self.extract_field(character_data, "name")
        race_value = await self.extract_field(character_data, "race")
        rtype_value = await self.extract_field(character_data, "race type")
        age_value = await self.extract_field(character_data, "age")
        gender_value = await self.extract_field(character_data, "gender")
        ki_value = await self.extract_field(character_data, "ki type")
        startingpl_value = await self.extract_field(character_data, "starting pl")

        results = {
            "requires_review": False,
            "admin_insights": [],
            "character_name": [name_value],
            "race": [race_value],
            "race_type": [rtype_value],
            "age": [age_value],
            "gender": [gender_value],
            "ki": [ki_value],
            "startingpl": [startingpl_value],
            "summary": summarizer.summarize_text(self.get_content(summary_fields), 4),
            "physcial": summarizer.summarize_text(self.get_content(physcial_fields), 2),
            "personality": summarizer.summarize_text(self.get_content(personality_fields), 2),
            "backstory": summarizer.summarize_text(self.get_content(backstory_fields), 4),
            "bullet_points": summarizer.summarize_bullet_points(agg_processed_sents, bullet_count),
            "verification_token": token
        }
        return source, results, starting_abilities
    
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