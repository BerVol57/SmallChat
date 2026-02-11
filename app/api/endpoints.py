from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, services
from app.core.database import get_db
import uuid

router = APIRouter()

@router.post("/sessions", response_model=schemas.SessionResponse)
def create_session(db: Session = Depends(get_db)):
    new_uuid = str(uuid.uuid4()) # Генеруємо випадковий ID
    db_session = models.ChatSession(session_uuid=new_uuid, total_cost=0.0)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@router.post("/sessions/{session_uuid}/chat")
async def chat(session_uuid: str, request: schemas.ChatRequest, db: Session = Depends(get_db)):
    # Шукаємо сесію
    session = db.query(models.ChatSession).filter(models.ChatSession.session_uuid == session_uuid).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found. Create one first via POST /sessions")
    # Отримуємо історію
    history = db.query(models.Message).filter(models.Message.session_id == session.id).all()

    # Запит до AI
    ai_data = await services.get_ai_response(request.message, history)

    # Зберігаємо повідомлення користувача
    user_msg = models.Message(
        session_id=session.id,
        role="user",
        content=request.message,
        tokens=0, # Для простоти вхідні токени окремо не пишемо, або рахуємо пізніше
        cost=0.0
    )
    db.add(user_msg)

    # Зберігаємо відповідь AI
    ai_msg = models.Message(
        session_id=session.id,
        role="assistant",
        content=ai_data["content"],
        tokens=ai_data["prompt_tokens"] + ai_data["completion_tokens"],
        cost=ai_data["cost"]
    )
    db.add(ai_msg)

    # Оновлюємо загальну вартість сесії
    session.total_cost += ai_data["cost"]
    
    db.commit()
    db.refresh(ai_msg)
    
    return ai_msg