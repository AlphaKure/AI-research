from src.utils.system import System

import psutil

class RAM:

    @classmethod
    def get_ram_status(cls):
        mem_info = psutil.virtual_memory()
        if System.operating_system == "Windows":
            return {"used": mem_info.used/ (1024**3), "total": mem_info.total/ (1024**3)}
        elif System.operating_system == "Linux":
            return{"used": (mem_info.total-mem_info.available)/ (1024**3), "total": mem_info.total/ (1024**3)}