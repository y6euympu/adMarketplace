from telethon import TelegramClient, types, functions, errors
import json


class MTProtoGateway:
    def __init__(self, project_path: str, identificator: int, hash: str):
        self.telegramClient = TelegramClient(f"{project_path}/mics/MTProtoSession", identificator, hash)
        self.identificator = identificator
        self.hash = hash
        self.project_path = project_path

    async def getClient(self, path: str) -> TelegramClient:
        return TelegramClient(f"{self.project_path}/mics/{path}", self.identificator, self.hash)
    
    async def stopBy(self, myCLient: TelegramClient) -> None:
        async with myCLient:
            return
    
    async def getFullChannelRequest(self, entity: str) -> types.messages.ChatFull:
        async with self.telegramClient:
            return await self.telegramClient(
                functions.channels.GetFullChannelRequest(entity)
            )

    async def getModers(self, entity: str) -> list[types.User]:
        async with self.telegramClient:
            return await self.telegramClient.get_participants(
                entity = entity, filter = types.ChannelParticipantsAdmins
            )

    async def getEntityStats(self, entity: str, requester: any = False) -> dict[str, list[str]|float]:
        async with self.telegramClient:
            request = functions.stats.GetBroadcastStatsRequest(
                await self.telegramClient.get_input_entity(entity)
            )

            try:
                entityStats = await self.telegramClient(request)
            except errors.StatsMigrateError as exception:
                requester = await self.telegramClient._borrow_exported_sender(exception.dc)
                entityStats = await requester.send(request)
            
            request = functions.stats.LoadAsyncGraphRequest(entityStats.languages_graph.token)

            if not (requester):
                localesGraph = await self.telegramClient(request)
            else:
                localesGraph = await requester.send(request)
                await self.telegramClient._return_exported_sender(requester)

            localesStats = json.loads(localesGraph.json.data)["names"]
            localesStats = [localesStats[key] for key in localesStats.keys()][:2]

            return {"localesStats": localesStats, "perPost": entityStats.views_per_post.current, "followers": entityStats.followers.current}