from typing import Optional, Union, Any, Tuple
import asyncpg
import psycopg2
from psycopg2.extras import DictCursor, DictRow
from core.config import DB_CONFIG
import logging

logger = logging.getLogger(__name__)

# -------------------- ASYNC PG POOL --------------------

pool: Optional[asyncpg.pool.Pool] = None

async def init_db_pool() -> asyncpg.pool.Pool:
    """
    Initialize asyncpg connection pool if not already created.
    """
    global pool
    if pool is None:
        # noinspection PyUnresolvedReferences
        pool = await asyncpg.create_pool(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database'],
            min_size=1,
            max_size=10
        )
        logger.info("Asyncpg pool created successfully.")
    return pool

async def fetch_query(query: str, params: Tuple = (), fetch: str = "all") -> Any:
    """
    Async fetch using asyncpg pool.
    :param query: SQL query
    :param params: Query parameters
    :param fetch: 'one' or 'all'
    :return: DictRow or list of rows
    """
    await init_db_pool()
    async with pool.acquire() as conn:
        if fetch == "one":
            result = await conn.fetchrow(query, *params) if params else await conn.fetchrow(query)
        else:
            result = await conn.fetch(query, *params) if params else await conn.fetch(query)
        logger.debug(f"Query executed: {query} | Params: {params}")
        return result

async def execute_command(query: str, params: Tuple = ()) -> str:
    """
    Async execute command (INSERT/UPDATE/DELETE) using asyncpg pool.
    :param query: SQL command
    :param params: parameters
    :return: result string
    """
    await init_db_pool()
    async with pool.acquire() as conn:
        result = await conn.execute(query, *params) if params else await conn.execute(query)
        logger.debug(f"Command executed: {query} | Params: {params}")
        return result

# -------------------- SYNC PSYCOPG2 --------------------

class DatabaseManager:
    """
    Synchronous database manager for legacy code.
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
            logger.error(f"Database error: {exc_val}")
        else:
            self.conn.commit()
            logger.info("Transaction committed successfully.")
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def execute(self, query: str, params: Union[tuple, dict, None] = None):
        self.cursor.execute(query, params)
        logger.debug(f"Executed query: {query} | Params: {params}")

    def fetchone(self, query: str, params: Union[tuple, dict, None] = None) -> Optional[DictRow]:
        self.cursor.execute(query, params)
        result = self.cursor.fetchone()
        logger.debug(f"Fetched one: {query} | Params: {params} | Result: {result}")
        return result

    def fetchall(self, query: str, params: Union[tuple, dict, None] = None) -> list[tuple[Any, ...]]:
        self.cursor.execute(query, params)
        result = self.cursor.fetchall()
        logger.debug(f"Fetched all: {query} | Params: {params} | Result count: {len(result)}")
        return result

def execute_query(
    query: str,
    params: Union[tuple, dict, None] = None,
    fetch: Optional[str] = None
) -> Optional[Union[DictRow, list[tuple[Any, ...]], bool]]:
    """
    Sync helper to execute queries using DatabaseManager.
    :param query: SQL query
    :param params: Query parameters
    :param fetch: 'one', 'all', or None for command
    :return: result or True for success, None if error
    """
    try:
        with DatabaseManager() as db:
            if fetch == "one":
                return db.fetchone(query, params)
            elif fetch == "all":
                return db.fetchall(query, params)
            else:
                db.execute(query, params)
                return True
    except psycopg2.Error as e:
        logger.error(f"Database execution error: {e}")
        return None