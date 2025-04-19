from pydantic import BaseModel
from typing import Literal

class GetOSInfo(BaseModel):

    operating_system: Literal["Windows", "Linux"]
    gpu_type: Literal["nvidia","amd","unknown"]