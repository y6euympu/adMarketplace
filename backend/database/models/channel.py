from sqlalchemy import Column, UUID, JSON, DateTime, text, ForeignKey, String

from .mics import Base


class Channel(Base):
    __tablename__ = 'channel'

    channel_id = Column(
        UUID(False), 
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    manager = Column(UUID(False), ForeignKey("participant.participant_id"))
    wallet = Column(String(255))
    entity = Column(JSON())
    registration_date = Column(
        DateTime, server_default=text("timezone('utc', now())")
    )