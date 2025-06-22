from fastapi import APIRouter ,Depends 
from sqlmodel import Session
from api.db import get_session
from api.chat.models import ChatMessagePAyload ,ChatMessage,ChatMessageListItem
from sqlmodel import select
router=APIRouter()

@router.get('/')
def chat_health():
    return {"status":"ok"}

@router.post('/',response_model=ChatMessageListItem)
def create_chat_message(
    payload:ChatMessagePAyload,
    session:Session=Depends(get_session)
    ):
    obj = ChatMessage(**payload.model_dump())
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

@router.get('/messages',response_model=list[ChatMessageListItem])
def get_chat_messages(
    session:Session=Depends(get_session)
    ):
    return session.exec(select(ChatMessage)).all()
