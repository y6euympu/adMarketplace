from aiogram import Router, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.methods import SendMessage
from aiogram.fsm.context import FSMContext

from core.container import Container


router = Router()

@router.message()
async def sendMessageFromUserToUser(message: Message, state: FSMContext) -> None:

    await message.answer("emptyEmptyEmptyEmpty")