import asyncpg
from typing import Optional
from infra.config.configuration import env


class DatabaseConnection:
    _instance: Optional["DatabaseConnection"] = None
    _pool: Optional[asyncpg.Pool] = None

    def __new__(cls) -> "DatabaseConnection":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    async def connect(cls) -> asyncpg.Pool:
        if cls._pool is None:
            cls._pool = await asyncpg.create_pool(
                host=env.DB_HOST,
                port=env.DB_PORT,
                user=env.DB_USER,
                password=env.DB_PASSWORD,
                database=env.DB_NAME,
                min_size=0,
                max_size=env.DB_POOL_MAX,
                timeout=5.0,
                command_timeout=30.0,
            )

            async with cls._pool.acquire() as connection:
                print("Connected to PostgreSQL successfully on port", env.DB_PORT)
        return cls._pool

    @classmethod
    async def disconnect(cls) -> None:
        if cls._pool is not None:
            await cls._pool.close()
            cls._pool = None

    @classmethod
    def get_pool(cls) -> asyncpg.Pool:
        if cls._pool is None:
            raise RuntimeError("Database pool has not been initialized. Call connect() first.")
        return cls._pool


db_connection = DatabaseConnection()

__all__ = ["DatabaseConnection", "db_connection"]
