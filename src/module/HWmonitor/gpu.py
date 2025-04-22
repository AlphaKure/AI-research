from src.utils.system import System

import subprocess
import re

class GPU:

    @classmethod
    def get_gpu_status(cls):
        if System.get_gpu_type() == "nvidia":
            return cls.get_gpu_status_nvidia()
        #elif System.get_gpu_type() == "amd":
        #    return cls.get_gpu_status_amd()
        else:
            return

    @classmethod
    def get_gpu_status_nvidia(cls):
        
        try:
            outputs = subprocess.check_output(["nvidia-smi","--query-gpu=name,temperature.gpu,memory.used,memory.total,utilization.gpu"],universal_newlines=True)
            outputs = outputs.strip().split("\n")[1:] # skip title
            info = []
            for output in outputs:
                output = output.strip().split(",")
                info.append({"device_name":output[0], "temperature":output[1], "vram_use":output[2], "vram_totel":output[3], "usage": output[4]})
            return info
        except:
            print("[ERROR] Nvidia GPU status fetch error")
            return []
        
