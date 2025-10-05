from infrastructure import CategoryRepository

class ViewCategoryQuery:
    def __init__(self, guild_id: str, category_name: str):
        self.repository = CategoryRepository()
        self.guild_id = guild_id
        self.category_name = category_name

    async def execute(self) -> dict:
        return await self.repository.get_by_name(self.guild_id, self.category_name)