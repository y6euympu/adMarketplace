from aiogram.types import TelegramObject, User
from aiogram import Dispatcher, Bot, Router
from aiogram.fsm.storage.memory import MemoryStorage

from typing import Callable, Dict, Any, Awaitable

from .handlers import handlers
from .misc import registr

from core.config import settings
from core.container import Container


class Gateway():
    def __init__(
            self, container: Container, handlers: list[Router]
        ) -> None:
        self.container = container

        self.bot = Bot(token=container.config.BOT_TOKEN)
        self.dispatcher = Dispatcher(
            storage=MemoryStorage()
        )

        for handler in handlers:
            self.dispatcher.include_router(handler)

        @self.dispatcher.update.outer_middleware()
        async def extensions(
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
        ) -> None:
            event_from_user: User = data['event_from_user']

            participant = await container.participant_repository.getEntryByEntity(
                event_from_user.id
            )
            if not participant:
                await registr(event_from_user, participant, container)

            data["container"] = container
            await handler(event, data)

    async def host(self) -> None:
        await self.container.reconnect()
        
        await self.dispatcher.start_polling(
            self.bot, allowed_updates=self.dispatcher.resolve_used_update_types()
        )

        await self.container.shutdown()


gateway = Gateway(container=Container(settings), handlers=handlers)