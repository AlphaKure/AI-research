from pathlib import Path
import platform
from typing import ClassVar,Literal

class System:

    root : ClassVar[Path] = Path(__file__).resolve().parent.parent # point to src

    operation_system: ClassVar[Literal["Windows","Linux"]] = platform.system()

    @classmethod
    def get_os_info(cls):
        return {"operation_system":cls.operation_system}