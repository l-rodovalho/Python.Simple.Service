from typing import Any, Optional
import asyncpg

class CustomerRepository:
    def __init__(self, pool: asyncpg.Pool) -> None:
        self.pool = pool

    async def find_by_id(self, customer_id: str) -> Optional[dict[str, Any]]:
        query = """
            SELECT cd_cliente, nome, endereco_cobranca 
            FROM cliente 
            WHERE cd_cliente = $1 AND ativo = true
        """
        
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(query, customer_id)

        if not row:
            return None

        return dict(row)


__all__ = ["CustomerRepository"]