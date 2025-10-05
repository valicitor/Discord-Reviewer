from infrastructure import CategoryRepository

class DeleteAllCategoriesCommand:
    def __init__(self, guild_id: str):
        self.repository = CategoryRepository()
        self.guild_id = guild_id

    async def execute(self) -> int:
        deleted_count = await self.repository.delete_all(self.guild_id)
        return deleted_count