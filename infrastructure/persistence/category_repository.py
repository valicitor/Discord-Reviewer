from infrastructure.interfaces.i_category_repository import ICategoryRepository
from typing import List
from uuid import UUID
import sqlite3
from datetime import datetime

class CategoryRepository(ICategoryRepository):
    def __init__(self, db_path='tiers.db'):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS tiers (
                id TEXT PRIMARY KEY,
                guild_id INTEGER,
                tier_name TEXT,
                prompt TEXT,
                priority INTEGER,
                created_at TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    async def get_by_id(self, id: UUID):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM tiers WHERE id = ?', (str(id),))
            return c.fetchone()

    async def get_all(self, guild_id: str) -> List[dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute('SELECT * FROM tiers WHERE guild_id = ?', (guild_id,))
            rows = c.fetchall()
            return [dict(row) for row in rows]

    async def list(self, guild_id: str) -> List[dict]:
        return await self.get_all(guild_id)

    async def add(self, entity: dict) -> None:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO tiers (id, guild_id, tier_name, prompt, priority, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (str(entity['id']), entity['guild_id'], entity['tier_name'], entity['prompt'], entity['priority'], datetime.now()))
            conn.commit()

    async def update(self, entity: dict) -> None:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''
                UPDATE tiers
                SET tier_name = ?, prompt = ?, priority = ?
                WHERE id = ?
            ''', (entity['tier_name'], entity['prompt'], entity['priority'], str(entity['id'])))
            conn.commit()

    async def delete(self, entity: dict) -> None:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('DELETE FROM tiers WHERE id = ?', (str(entity['id']),))
            conn.commit()

    async def delete_all(self, guild_id: str) -> int:
        """Delete all categories for a guild and return the number of deleted records"""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('DELETE FROM tiers WHERE guild_id = ?', (guild_id,))
            deleted_count = c.rowcount  # number of rows deleted
            conn.commit()
            return deleted_count

    async def exists(self, id: UUID) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT 1 FROM tiers WHERE id = ?', (str(id),))
            return c.fetchone() is not None

    async def get_by_name(self, guild_id: str, name: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute('SELECT * FROM tiers WHERE guild_id = ? AND tier_name = ?', (guild_id, name,))
            return c.fetchone()

    async def name_exists(self, guild_id: str, name: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT 1 FROM tiers WHERE guild_id = ? AND tier_name = ?', (guild_id, name,))
            return c.fetchone() is not None