from typing import Optional

from pydantic import BaseModel, constr

class Message(BaseModel):
    message: str
    status: str = 'ok'