from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None


class TaskRead(TaskCreate):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class NoteCreate(BaseModel):
    title: str
    content: str


class NoteRead(NoteCreate):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
