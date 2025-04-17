from pydantic import BaseModel
from typing import Literal

class GetOSInfo(BaseModel):
    
    operation_system: Literal["Windows", "Linux"]