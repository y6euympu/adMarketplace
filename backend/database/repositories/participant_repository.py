from database.models.metadata import metadata
from database.models.participant import Participant

from databases import Database

from sqlalchemy.orm import Query
from sqlalchemy import Table

from .repository import Repository


class ParticipantRepository(Repository[Participant]):
    model = Participant
    table: Table

    def __init__(self, database: Database):
        super().__init__(database)
        self.table = metadata.tables["participant"]

    async def entry(self, entity_id: int) -> Participant | None:
        query: Query = self.table.insert().values(
            entity_id=entity_id
        ).returning(self.table)
        return self.to_model(await self.database.fetch_one(query=query))
    
    async def getEntry(self, participant_id: str) -> Participant | None:
        query: Query = self.table.select().where(
            participant_id == self.table.c.participant_id
        )
        return self.to_model(await self.database.fetch_one(query=query))

    async def getEntryByEntity(self, entity_id: int) -> Participant | None:
        query: Query = self.table.select().where(
            entity_id == self.table.c.entity_id
        )
        return self.to_model(await self.database.fetch_one(query=query))