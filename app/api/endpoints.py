from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app import models, schemas, services
from app.core.database import get_db
import uuid

router = APIRouter()

@router.get("/new_session")
async def quick_start(db: Session = Depends(get_db)):
    new_uuid = str(uuid.uuid4())
    db_session = models.ChatSession(session_uuid=new_uuid, total_cost=0.0)
    db.add(db_session)
    db.commit()
    return RedirectResponse(url=f"/static/index.html?session={new_uuid}")

@router.post("/sessions", response_model=schemas.SessionResponse)
def create_session(db: Session = Depends(get_db)):
    new_uuid = str(uuid.uuid4())
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

# Повне видалення сесії та всіх її повідомлень
@router.delete("/sessions/{session_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(session_uuid: str, db: Session = Depends(get_db)):
    session = db.query(models.ChatSession).filter(models.ChatSession.session_uuid == session_uuid).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Видаляємо всі пов'язані повідомлення
    db.query(models.Message).filter(models.Message.session_id == session.id).delete()
    
    # Видаляємо саму сесію
    db.delete(session)
    db.commit()
    return None

# Скидання чату (видалення повідомлень, але збереження UUID)
@router.post("/sessions/{session_uuid}/reset", response_model=schemas.SessionResponse)
def reset_session(session_uuid: str, db: Session = Depends(get_db)):
    session = db.query(models.ChatSession).filter(models.ChatSession.session_uuid == session_uuid).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Видаляємо всі повідомлення цієї сесії
    db.query(models.Message).filter(models.Message.session_id == session.id).delete()
    
    # Скидаємо накопичену вартість
    session.total_cost = 0.0
    
    db.commit()
    db.refresh(session)
    return session

@router.get("/sessions/{session_uuid}/history", response_model=schemas.SessionResponse)
def get_history(session_uuid: str, db: Session = Depends(get_db)):
    session = db.query(models.ChatSession).filter(models.ChatSession.session_uuid == session_uuid).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.get("/debug/all-sessions")
def get_all_sessions(db: Session = Depends(get_db)):
    # Повертає абсолютно всі сесії, які є в БД
    return db.query(models.ChatSession).all()