from domain import IRepository

class IPrefixRepository(IRepository):
    async def get_by_guild_id(self, guild_id: str):
        """Get prfix by a specific guild."""
        raise NotImplementedError("This method should be implemented by subclasses")

    async def upsert_prefix(self, guild_id: str, prefix: str):
      """Upsert a prefix."""
      raise NotImplementedError("This method should be implemented by subclasses")