from typing import ClassVar
from pathlib import Path

class System:

    root : ClassVar[Path] = Path(__file__).resolve().parent.parent # point to src