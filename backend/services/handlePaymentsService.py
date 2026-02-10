from database.repositories.wallet_repository import WalletRepository
from database.repositories.invoice_repository import InvoiceRepository
from database.repositories.payment_repository import PaymentRepository

from database.models.payment import Payment

from gateways.blockchainsGateway import BlockchainsGateway

from decimal import Decimal

from datetime import datetime, timedelta, timezone
from asyncio import sleep


class HandlePaymentsService:
    def __init__(
        self,
        wallet_repository: WalletRepository,
        invoice_repository: InvoiceRepository,
        payment_repository: PaymentRepository,
        blockchainsGateway: BlockchainsGateway
    ):
        self.wallet_repository = wallet_repository
        self.invoice_repository = invoice_repository
        self.payment_repository = payment_repository
        self.blockchainsGateway = blockchainsGateway

    async def entryPayment(self, purchaser: str, salesman: str, quantum: Decimal) -> PaymentRepository:
        wallet = await self.blockchainsGateway.generateWallet()
        wallet = await self.wallet_repository.entry(
            wallet["walletHash"], {"mnemonics" : wallet["mnemonics"]}
        )

        invoice = await self.invoice_repository.entry(
            wallet.wallet, "empty", Decimal(f"{quantum}"), Decimal("0.08")
        )

        payment = await self.payment_repository.entry(
            invoice.invoice_id, purchaser, salesman
        )

    async def handleInvoices(self) -> None:
        invoices = await self.invoice_repository.getEntrysByStatus("waiting")

        for invoice in invoices:
            invoiceWallet = await self.wallet_repository.getEntry(invoice.wallet)
            walletBalance = await self.blockchainsGateway.getBalance(invoiceWallet.hash)

            if walletBalance in [invoice.quantum + invoice.fee]:
                await self.invoice_repository.updateStatus(invoice.invoice_id, "payed")

            await sleep(0.8)
            
            if (datetime.now(timezone.utc) - invoice.invoice_date) > (timedelta(minutes=16)):
                await self.invoice_repository.updateStatus(invoice.invoice_id, "expired")
            
    async def handleInvoicesDaemon(self) -> None:
        while True:
            await self.handleInvoices()

    async def handlePayments(self) -> None:
        paymetns = await self.payment_repository.getEntrysByStatus("waiting")

        for payment in paymetns:
            paymentInvoice = await self.invoice_repository.getEntry(payment.invoice_id)

            await sleep(0.8)

            if paymentInvoice.status not in ["waiting"]:
                await self.payment_repository.updateStatus(payment.payment_id, paymentInvoice.status)

    async def handlePaymentsDaemon(self) -> None:
        while True:
            await self.handlePayments()