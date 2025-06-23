import os
from langchain_openai import ChatOpenAI
from pydantic import BaseModel , Field
from dotenv import load_dotenv
load_dotenv()

OPENAI_MODEL_NAME=os.getenv("OPENAI_MODEL_NAME")
OPENAI_BASE_URL=os.getenv("OPENAI_BASE_URL")
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")


class EmailMessage(BaseModel):
    subject: str = Field(description="The subject of the email")
    contents: str = Field(description="The contents of the email")
    invalid_requests: bool | None = Field(default=None, description="Whether the email is invalid")


llm_base = ChatOpenAI(
    model_name=OPENAI_MODEL_NAME,
    openai_api_key=OPENAI_API_KEY,
    openai_api_base=OPENAI_BASE_URL)


llm=llm_base.with_structured_output(EmailMessage)

messages=[
    {"role":"system","content":"You are a helpful assistant. for research and composing plaintext emails."},
    {"role":"user","content":"Write a email on ai for education"}
]

email_message=llm.invoke(messages)
print(email_message)
