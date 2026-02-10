from database.models.metadata import metadata
from database.models.payment import Payment

from databases import Database

from sqlalchemy.orm import Query
from sqlalchemy import Table

from .repository import Repository


class PaymentRepository(Repository[Payment]):
    model = Payment
    table: Table

    def __init__(self, database: Database):
        super().__init__(database)
        self.table = metadata.tables["payment"]

    async def entry(self, invoice_id: str, purchaser: str, salesman: str) -> Payment | None:
        query: Query = self.table.insert().values(
            invoice_id = invoice_id, purchaser = purchaser, salesman = salesman
        ).returning(self.table)
        return self.to_model(await self.database.fetch_one(query=query))
    
    async def getEntry(self, payment_id: str) -> Payment | None:
        query: Query = self.table.select().where(
            payment_id == self.table.c.payment_id
        )
        return self.to_model(await self.database.fetch_one(query=query))
    
    async def getEntrysByStatus(self, status: str) -> list[Payment]:
        query: Query = self.table.select().where(
            status == self.table.c.status
        )
        return self.to_models(await self.database.fetch_all(query=query))
    
    async def updateStatus(self, payment_id: str, status: str) -> None:
        query: Query = (
            self.table
            .update()
            .where(payment_id == self.table.c.payment_id)
            .values(status=status)
            .returning(self.table)
        )
        return self.to_model(await self.database.fetch_one(query=query))
