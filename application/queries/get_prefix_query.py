from infrastructure import PrefixRepository

class GetPrefixQuery:
    def __init__(self, guild_id: str):
        self.repository = PrefixRepository()
        self.guild_id = guild_id

    async def execute(self) -> str:
        prefix = await self.repository.get_by_guild_id(self.guild_id)
        return prefix or "!"