from pydantic import BaseModel , Field


class EmailMessage(BaseModel):
    subject: str = Field(description="The subject of the email")
    contents: str = Field(description="The contents of the email")
    invalid_requests: bool | None = Field(default=None, description="Whether the email is invalid")

class SupervisorMessageSchema(BaseModel):
    content: str