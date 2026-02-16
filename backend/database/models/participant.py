from sqlalchemy import Column, UUID, JSON, DateTime, text, BigInteger

from .mics import Base


class Participant(Base):
    __tablename__ = 'participant'

    participant_id = Column(
        UUID(False), 
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    jwt = Column(
        UUID(False), server_default=text("gen_random_uuid()")
    )
    entity_id = Column(BigInteger)
    entity = Column(JSON())
    registration_date = Column(
        DateTime, server_default=text("timezone('utc', now())")
    )