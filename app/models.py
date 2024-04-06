from sqlalchemy import Column, ForeignKey, String, UUID, DateTime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from base64 import urlsafe_b64encode

from .database import Base


class Note(Base):
    __tablename__ = "Notes"

    id = Column(UUID, primary_key=True)
    title = Column(String)
    permission = Column(String)
    ownerId = Column(String, ForeignKey("Users.id"))
    lastchangeAt = Column(DateTime)

    owner = relationship("User", back_populates="notes")

    @hybrid_property
    def url(self) -> String:
        return urlsafe_b64encode(self.id.bytes).decode("ascii")


class User(Base):
    __tablename__ = "Users"

    id = Column(UUID, primary_key=True)
    email = Column(String)
    notes = relationship("Note", back_populates="owner")
