from database.models.metadata import metadata
from database.models.wallet import Wallet

from databases import Database

from sqlalchemy.orm import Query
from sqlalchemy import Table

from .repository import Repository


class WalletRepository(Repository[Wallet]):
    model = Wallet
    table: Table

    def __init__(self, database: Database):
        super().__init__(database)
        self.table = metadata.tables["wallet"]

    async def entry(self, hash: str, secret: dict[str,list[str]]) -> Wallet | None:
        query: Query = self.table.insert().values(
            hash = hash, secret = secret
        ).returning(self.table)
        return self.to_model(await self.database.fetch_one(query=query))
    
    async def getEntry(self, wallet: str) -> Wallet | None:
        query: Query = self.table.select().where(
            wallet == self.table.c.wallet
        )
        return self.to_model(await self.database.fetch_one(query=query))
    
    async def getEntryByHash(self, hash: str) -> Wallet | None:
        query: Query = self.table.select().where(
            hash == self.table.c.hash
        )
        return self.to_model(await self.database.fetch_one(query=query))
