from database.repositories.participant_repository import ParticipantRepository
from database.repositories.wallet_repository import WalletRepository
from database.repositories.invoice_repository import InvoiceRepository
from database.repositories.payment_repository import PaymentRepository

from gateways.MTProtoGateway import MTProtoGateway
from gateways.blockchainsGateway import BlockchainsGateway

from services.handlePaymentsService import HandlePaymentsService

from .singleton import Singleton
from .config import Settings

from databases import Database


class BaseContainer:
    _database: Database | None = None
    _config: Settings

    _participant_repository: ParticipantRepository | None = None
    _wallet_repository: WalletRepository | None = None
    _invoice_repository: InvoiceRepository | None = None
    _payment_repository: PaymentRepository | None = None

    _MTProtoGateway: MTProtoGateway | None = None
    _blockchainsGateway: BlockchainsGateway | None = None

    _handlePaymentsService: HandlePaymentsService | None = None

    def __init__(self, config: Settings):
        self._config = config

    async def reconnect(self) -> None:
        if not self.database.is_connected:
            await self.database.connect()

    async def shutdown(self) -> None:
        if self.database.is_connected:
            await self.database.disconnect()

    @property
    def database(self) -> Database:
        if self._database is None:
            self._database = Database(self.config.DATABASE_URL)
        return self._database
    
    @property
    def config(self) -> Settings:
        return self._config
    
    @property
    def participant_repository(self) -> ParticipantRepository:
        if self._participant_repository is None:
            self._participant_repository = ParticipantRepository(
                database=self.database
            )
        return self._participant_repository
    
    @property
    def wallet_repository(self) -> WalletRepository:
        if self._wallet_repository is None:
            self._wallet_repository = WalletRepository(
                database=self.database
            )
        return self._wallet_repository
    
    @property
    def invoice_repository(self) -> InvoiceRepository:
        if self._invoice_repository is None:
            self._invoice_repository = InvoiceRepository(
                database=self.database
            )
        return self._invoice_repository
    
    @property
    def payment_repository(self) -> PaymentRepository:
        if self._payment_repository is None:
            self._payment_repository = PaymentRepository(
                database=self.database
            )
        return self._payment_repository
    
    @property
    def MTProtoGateway(self) -> MTProtoGateway:
        if self._MTProtoGateway is None:
            self._MTProtoGateway = MTProtoGateway(
                identificator=self.config.TELEGRAM_APPLICATION_API_ID,
                project_path=self.config.PATH,
                hash=self.config.TELEGRAM_APPLICATION_API_HASH
            )
        return self._MTProtoGateway
    
    @property
    def blockchainsGateway(self) -> BlockchainsGateway:
        if self._blockchainsGateway is None:
            self._blockchainsGateway = BlockchainsGateway(
                key=self.config.TONCENTER_API_KEY
            )
        return self._blockchainsGateway
    
    @property
    def handlePaymentsService(self) -> HandlePaymentsService:
        if self._handlePaymentsService is None:
            self._handlePaymentsService = HandlePaymentsService(
                wallet_repository=self.wallet_repository,
                invoice_repository=self.invoice_repository,
                payment_repository=self.payment_repository,
                blockchainsGateway=self.blockchainsGateway
            )
        return self._handlePaymentsService


class Container(BaseContainer, metaclass=Singleton):
    pass


class DevContainer(BaseContainer):
    pass