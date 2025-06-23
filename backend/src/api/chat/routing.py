from email import message
from fastapi import APIRouter ,Depends 
from sqlmodel import Session
from api.db import get_session
from api.chat.models import ChatMessagePAyload ,ChatMessage,ChatMessageListItem
from api.ai.services import generate_email_messages
from api.ai.schemas import EmailMessage,SupervisorMessageSchema
from api.ai.agent import get_supervisor
from sqlmodel import select
router=APIRouter()

@router.get('/')
def chat_health():
    return {"status":"ok"}

@router.post('/',response_model=SupervisorMessageSchema)
def create_chat_message(
    payload:ChatMessagePAyload,
    session:Session=Depends(get_session)
    ):
    obj = ChatMessage(**payload.model_dump())
    session.add(obj)
    session.commit()
    #session.refresh(obj)
    #email_message=generate_email_messages(payload.message)
    sup=get_supervisor()
    msg_data={
        "messages":[
            {
                "role":"user",
                "content":payload.message
            }
        ]
    }
    response=sup.invoke(msg_data)
    message=response.get('messages')
    return message[-1]

@router.get('/messages',response_model=list[ChatMessageListItem])
def get_chat_messages(
    session:Session=Depends(get_session)
    ):
    return session.exec(select(ChatMessage)).all()
