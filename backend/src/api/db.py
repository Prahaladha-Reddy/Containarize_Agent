import os
import sqlmodel
from sqlmodel import Session,SQLModel
DATABASE_URL = os.getenv("DATABASE_URL")

engine=sqlmodel.create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

async def init_db():
    print("creating database tables ..")
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully")