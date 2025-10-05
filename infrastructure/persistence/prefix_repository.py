from infrastructure.interfaces.i_prefix_repository import IPrefixRepository
from typing import List, Optional
from uuid import UUID, uuid4
import sqlite3
from datetime import datetime

class PrefixRepository(IPrefixRepository):
    def __init__(self, db_path='tiers.db'):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS prefixes (
                id TEXT PRIMARY KEY,
                guild_id INTEGER UNIQUE,
                prefix TEXT NOT NULL,
                created_at TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    async def get_by_id(self, id: UUID) -> Optional[dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute('SELECT * FROM prefixes WHERE id = ?', (str(id),))
            row = c.fetchone()
            return dict(row) if row else None

    async def get_all(self, guild_id: str) -> List[dict]:
        # one per guild normally, but return as list for IRepository contract
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute('SELECT * FROM prefixes WHERE guild_id = ?', (guild_id,))
            rows = c.fetchall()
            return [dict(row) for row in rows]

    async def list(self, guild_id: str) -> List[dict]:
        return await self.get_all(guild_id)

    async def add(self, entity: dict) -> None:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO prefixes (id, guild_id, prefix, created_at)
                VALUES (?, ?, ?, ?)
            ''', (str(entity['id']), entity['guild_id'], entity['prefix'], datetime.now()))
            conn.commit()

    async def update(self, entity: dict) -> None:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''
                UPDATE prefixes
                SET prefix = ?
                WHERE id = ?
            ''', (entity['prefix'], str(entity['id'])))
            conn.commit()

    async def delete(self, entity: dict) -> None:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('DELETE FROM prefixes WHERE id = ?', (str(entity['id']),))
            conn.commit()

    async def exists(self, id: UUID) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT 1 FROM prefixes WHERE id = ?', (str(id),))
            return c.fetchone() is not None

    # convenience: get prefix by guild_id (used in get_prefix callable)
    async def get_by_guild_id(self, guild_id: str) -> Optional[str]:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT prefix FROM prefixes WHERE guild_id = ?', (guild_id,))
            row = c.fetchone()
            return row[0] if row else None

    # convenience: upsert prefix
    async def upsert_prefix(self, guild_id: str, prefix: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO prefixes (id, guild_id, prefix, created_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(guild_id) DO UPDATE SET prefix = excluded.prefix
            ''', (str(uuid4()), guild_id, prefix, datetime.now()))
            conn.commit()
