from domain import IRepository

class ICategoryRepository(IRepository):
    async def delete_all(self, guild_id: str):
        """Delete all categories for a specific guild."""
        raise NotImplementedError("This method should be implemented by subclasses")
    
    async def get_by_name(self, guild_id: str, name: str):
      """Retrieve a tier by its name."""
      raise NotImplementedError("This method should be implemented by subclasses")
    
    async def name_exists(self, guild_id: str, name: str) -> bool:
      """Check if a tier name already exists."""
      raise NotImplementedError("This method should be implemented by subclasses")