from infrastructure import PrefixRepository

class UpsertPrefixCommand:
    def __init__(self, guild_id: str, prefix: str):
        self.repository = PrefixRepository()
        self.guild_id = guild_id
        self.prefix = prefix

    async def execute(self) -> bool:
        await self.repository.upsert_prefix(self.guild_id, self.prefix)
        prefix = await self.repository.get_by_guild_id(self.guild_id)
        return prefix == self.prefix