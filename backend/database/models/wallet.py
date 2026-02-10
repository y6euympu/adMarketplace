from sqlalchemy import Column, String, UUID, JSON, text

from .mics import Base


class Wallet(Base):
    __tablename__ = 'wallet'

    wallet = Column(
        UUID(False),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    hash = Column(String(255))
    secret = Column(JSON())
    blockchain = Column(String(255))

