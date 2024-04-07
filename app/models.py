from sqlalchemy import Column, ForeignKey, String, UUID, DateTime, Uuid
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from base64 import urlsafe_b64encode, urlsafe_b64decode

from .database import Base


class Note(Base):
    __tablename__ = "Notes"

    id = Column(UUID, primary_key=True)
    title = Column(String)
    permission = Column(String)
    ownerId = Column(String, ForeignKey("Users.id"))
    lastchangeAt = Column(DateTime)
    content = Column(String)

    owner = relationship("User", back_populates="notes")

    @hybrid_property
    def url(self) -> String:
        return urlsafe_b64encode(self.id.bytes).decode("ascii")


class User(Base):
    __tablename__ = "Users"

    id = Column(UUID, primary_key=True)
    email = Column(String)
    notes = relationship("Note", back_populates="owner")


def from_url(encoded_id: str):
    import uuid

    missing_padding = len(encoded_id) % 4
    if missing_padding:
        encoded_id += "=" * (4 - missing_padding)
    try:
        return uuid.UUID(bytes=urlsafe_b64decode(encoded_id))
    except Exception:
        return None
