from core.container import Container
from core.config import settings

from asyncio import run


async def handleInvoicesDaemon(container: Container):
    await container.reconnect()

    await container.handlePaymentsService.handleInvoicesDaemon()
    await container.shutdown()


if __name__ == "__main__" :
    run(handleInvoicesDaemon(Container(settings)))