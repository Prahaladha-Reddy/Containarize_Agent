from email import message
from sqlmodel import SQLModel ,Field,DateTime
from datetime import datetime,timezone

def get_utc_time():
    return datetime.now().replace(tzinfo=timezone.utc)


class ChatMessagePAyload(SQLModel):
    message:str


class ChatMessage(SQLModel,table=True):
    id: int | None=Field(default=None,primary_key=True)
    message:str
    created_at:datetime=Field(
        default_factory=get_utc_time,
        sa_type=DateTime(timezone=True),
        nullable=False,
        primary_key=False
    )


class ChatMessageListItem(SQLModel):
    message:str
    created_at:datetime