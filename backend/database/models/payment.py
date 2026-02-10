from sqlalchemy import Column, ForeignKey, Enum, UUID, text

from .mics import Base


class Payment(Base):
    __tablename__ = 'payment'

    payment_id = Column(
        UUID(False),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    invoice_id = Column(UUID(False), ForeignKey("invoice.invoice_id"))
    purchaser = Column(UUID(False), ForeignKey("participant.participant_id"))
    salesman = Column(UUID(False), ForeignKey("participant.participant_id"))
    status = Column(
        Enum("waiting", "fetch", "payed", "expired", name="swap_status"), 
        server_default="waiting"
    )