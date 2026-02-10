from core.container import Container
from core.config import settings

from asyncio import run


async def handlePaymentsDaemon(container: Container):
    await container.reconnect()

    await container.handlePaymentsService.handlePaymentsDaemon()
    await container.shutdown()


if __name__ == "__main__" :
    run(handlePaymentsDaemon(Container(settings)))