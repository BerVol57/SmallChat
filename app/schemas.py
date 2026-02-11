from pydantic import BaseModel
from typing import List, Optional

class MessageBase(BaseModel):
    role: str # 'user' або 'assistant'
    content: str

class MessageResponse(MessageBase):
    tokens: int
    cost: float

    class Config:
        from_attributes = True

class SessionResponse(BaseModel):
    session_uuid: str
    total_cost: float
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str