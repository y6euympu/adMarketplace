from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.methods import SendMessage


router = Router()

@router.message(F.text.in_(["/start"]))
async def reverance(message: Message, bot: Bot) -> None:
    await bot(
        SendMessage(
            text="Project adMarketplace", chat_id=message.chat.id
        )
    )