from pydantic import BaseModel, Field


class InvitationAcceptResponse(BaseModel):
    invitation_id: str = Field(...)
    assignment_id: str = Field(...)
    accepted: bool = Field(...)
    message: str = Field(...)
