from pathlib import Path
import platform
from functools import lru_cache
from typing import ClassVar,Literal

class System:

    root : ClassVar[Path] = Path(__file__).resolve().parent.parent # point to src

    operation_system: ClassVar[Literal["Windows","Linux"]] = platform.system()
    
    @classmethod
    @lru_cache(maxsize=1) # 只運算一次
    def is_wsl(cls) -> bool:
        if cls.operation_system == "Windows":
            return False
        else:
            if "microsoft" or "wsl" in platform.uname().release.lower():
                return True
            return False

    @classmethod
    def get_os_info(cls):
        return {"operation_system":cls.operation_system,"is_wsl":cls.is_wsl()}