from database.models.metadata import metadata
from database.models.invoice import Invoice

from databases import Database

from sqlalchemy.orm import Query
from sqlalchemy import Table

from decimal import Decimal

from .repository import Repository


class InvoiceRepository(Repository[Invoice]):
    model = Invoice
    table: Table

    def __init__(self, database: Database):
        super().__init__(database)
        self.table = metadata.tables["invoice"]

    async def entry(self, wallet: str, cy: str, quantum: Decimal, fee: Decimal) -> Invoice | None:
        query: Query = self.table.insert().values(
            wallet = wallet, cy = cy, quantum = quantum, fee=fee
        ).returning(self.table)
        return self.to_model(await self.database.fetch_one(query=query))
    
    async def getEntry(self, invoice_id: str) -> Invoice | None:
        query: Query = self.table.select().where(
            invoice_id == self.table.c.invoice_id
        )
        return self.to_model(await self.database.fetch_one(query=query))
    
    async def getEntrysByStatus(self, status: str) -> list[Invoice]:
        query: Query = self.table.select().where(
            status == self.table.c.status
        )
        return self.to_models(await self.database.fetch_all(query=query))
    
    async def updateStatus(self, invoice_id: str, status: str) -> None:
        query: Query = (
            self.table
            .update()
            .where(invoice_id == self.table.c.invoice_id)
            .values(status=status)
            .returning(self.table)
        )
        return self.to_model(await self.database.fetch_one(query=query))


