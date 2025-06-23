import os
from langchain_openai import ChatOpenAI
from api.ai.schemas import EmailMessage

OPENAI_MODEL_NAME=os.getenv("OPENAI_MODEL_NAME")
OPENAI_BASE_URL=os.getenv("OPENAI_BASE_URL")
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")


def get_openai_llm():
    llm_base = ChatOpenAI(
    model_name=OPENAI_MODEL_NAME,
    openai_api_key=OPENAI_API_KEY,
    openai_api_base=OPENAI_BASE_URL)
    return llm_base
