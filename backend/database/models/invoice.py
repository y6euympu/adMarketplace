from sqlalchemy import Column, String, DECIMAL, DateTime, Enum, ForeignKey, UUID, text

from .mics import Base


class Invoice(Base):
    __tablename__ = 'invoice'

    invoice_id = Column(
        UUID(False),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    wallet = Column(UUID(False), ForeignKey("wallet.wallet"))
    cy = Column(String(255))
    quantum = Column(DECIMAL)
    fee = Column(DECIMAL)
    status = Column(
        Enum("waiting", "payed", "expired", name="payment_status"),
        server_default="waiting"
    )
    invoice_date = Column(
        DateTime(timezone=True), server_default=text("timezone('utc', now())")
    )

