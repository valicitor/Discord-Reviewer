from uuid import uuid4
from infrastructure import CategoryRepository

class CreateCategoryCommand:
    def __init__(self, guild_id: str, category_name: str, category_priority: int, category_prompt: str):
        self.repository = CategoryRepository()
        self.guild_id = guild_id
        self.category_name = category_name
        self.category_priority = category_priority
        self.category_prompt = category_prompt

    async def execute(self) -> bool:
        id = uuid4()
        entity = {
            'id': str(id),
            'guild_id': self.guild_id,
            'tier_name': self.category_name,
            'prompt': self.category_prompt,
            'priority': self.category_priority
        }
        await self.repository.add(entity)
        return await self.repository.exists(id)