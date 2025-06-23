from api.ai.llms import get_openai_llm
from api.ai.schemas import EmailMessage

def generate_email_messages(query:str)->EmailMessage:
    llm=get_openai_llm()
    llm=llm.with_structured_output(EmailMessage)
    messages=[
        {"role":"system","content":"You are a helpful assistant. for research and composing plaintext emails."},
        {"role":"user","content":query}
    ]
    return llm.invoke(messages)
    