from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List
from uuid import UUID

T = TypeVar('T')

class IRepository(ABC, Generic[T]):
    @abstractmethod
    async def get_by_id(self, id: UUID) -> T:
        pass

    @abstractmethod
    async def get_all(self, guild_id: str) -> List[T]:
        pass

    @abstractmethod
    async def list(self, guild_id: str) -> List[T]:
        pass

    @abstractmethod
    async def add(self, entity: T) -> None:
        pass

    @abstractmethod
    async def update(self, entity: T) -> None:
        pass

    @abstractmethod
    async def delete(self, entity: T) -> None:
        pass

    @abstractmethod
    async def exists(self, id: UUID) -> bool:
        pass