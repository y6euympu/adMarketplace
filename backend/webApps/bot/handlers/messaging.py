from aiogram import Router, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.methods import SendMessage

from core.container import Container


router = Router()

@router.message(StateFilter(None))
async def sendMessageFromUserToUser(message: Message) -> None:
    await message.answer("emptyEmptyEmptyEmpty")