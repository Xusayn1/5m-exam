from typing import Optional, Union, Any

import asyncpg
import psycopg2
from psycopg2.extras import DictCursor, DictRow

from core.config import DB_CONFIG


class DatabaseManager:
    """
    Database manager class to execute all queries
    """

    def __init__(self):
        self.conn: Optional[psycopg2.extensions.connection] = None
        self.cursor: Optional[psycopg2.extensions.cursor] = None

    def __enter__(self) -> "DatabaseManager":
        self.conn = psycopg2.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor(cursor_factory=DictCursor)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()

        if self.conn:
            self.conn.close()

        if self.cursor:
            self.cursor.close()

    def execute(self, query: str, params: Union[tuple, dict, None] = None):
        self.cursor.execute(query, params)

    def fetchone(self, query: str, params: Union[tuple, dict, None] = None) -> Optional[DictRow]:
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetchall(self, query: str, params: Union[tuple, dict, None] = None) -> list[tuple[Any, ...]]:
        self.cursor.execute(query, params)
        return self.cursor.fetchall()


def execute_query(
        query: str,
        params: Union[tuple, dict, None] = None,
        fetch: Union[str, None] = None
) -> DictRow | None | list[tuple[Any, ...]] | bool:
    try:
        with DatabaseManager() as db:
            if fetch == "one":
                return db.fetchone(query=query, params=params)
            elif fetch == "all":
                return db.fetchall(query=query, params=params)
            else:
                db.execute(query=query, params=params)
                return True
    except psycopg2.Error as e:
        print(e)
        return None


async def get_connection():
    return await asyncpg.connect(
        user="postgres",
        password="1234",
        database="postgres",
        host="localhost"
    )

async def fetch_query(query: str, params: tuple = ()):
    conn = await get_connection()
    try:
        return await conn.fetch(query, *params)
    finally:
        await conn.close()

async def execute_command(query: str, params: tuple = ()):
    conn = await get_connection()
    try:
        return await conn.execute(query, *params)
    finally:
        await conn.close()

