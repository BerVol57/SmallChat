from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class ChatSession(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    session_uuid = Column(String, unique=True, index=True)
    total_cost = Column(Float, default=0.0)
    messages = relationship("Message", back_populates="session")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    role = Column(String) # user/assistant
    content = Column(Text)
    tokens = Column(Integer)
    cost = Column(Float)
    session = relationship("ChatSession", back_populates="messages")