from database.models.participant import Participant
from core.container import Container

from aiogram.types import TelegramObject


async def registr(
    event_from_user: TelegramObject, participant: Participant, container: Container
) -> None:
    registr = await container.participant_repository.entry(
        event_from_user.id
    )