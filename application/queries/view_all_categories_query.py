from typing import List
from infrastructure import CategoryRepository

class ViewAllCategoriesQuery:
    def __init__(self, guild_id: str):
        self.repository = CategoryRepository()
        self.guild_id = guild_id

    async def execute(self) -> List[dict]:
        return await self.repository.get_all(self.guild_id)