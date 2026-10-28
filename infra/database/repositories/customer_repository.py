import json
from typing import Optional
import asyncpg

class CustomerRepository:
    def __init__(self, pool: asyncpg.Pool) -> None:
        self.pool = pool

    async def find_by_id(self, customer_id: str) -> Optional[dict]:
        query = """
            SELECT cd_cliente, nome, endereco_cobranca 
            FROM cliente 
            WHERE cd_cliente = $1 AND ativo = true
        """
        
        async with self.pool.acquire(timeout=5.0) as connection:
            row = await connection.fetchrow(query, customer_id)

        if not row:
            return None

        address = json.loads(row["endereco_cobranca"])
        history = address.get("billingHistory") if isinstance(address, dict) else None

        return {
            "customer_id": str(row["cd_cliente"]),
            "name": row["nome"],
            "bills": history if isinstance(history, list) else [],
        }


__all__ = ["CustomerRepository"]