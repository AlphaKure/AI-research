from src.utils.system import System
from src.schemas.outputs import system_schemas

from fastapi import APIRouter

router = APIRouter(
    tags= ["Enviroment"]
)

@router.get("/os", response_model=system_schemas.GetOSInfo)
def get_os_info():
    return System.get_os_info()