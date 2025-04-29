from src.utils.system import System

import subprocess
import re

class GPU:

    @classmethod
    def get_gpu_status(cls):
        if System.get_gpu_type() == "nvidia":
            return cls.get_gpu_status_nvidia()
        elif System.get_gpu_type() == "amd":
            return cls.get_gpu_status_amd()
        else:
            return

    @classmethod
    def get_gpu_status_nvidia(cls):
        
        try:
            outputs = subprocess.check_output(["nvidia-smi","--query-gpu=name,temperature.gpu,memory.used,memory.total,utilization.gpu","--format=csv"],universal_newlines=True)
            outputs = outputs.strip().split("\n")[1:] # skip title
            info = []
            for output in outputs:
                output = output.strip().split(",")
                info.append({"device_name":output[0], "temperature":output[1], "vram_use":output[2], "vram_totel":output[3], "usage": output[4]})
            return info
        except:
            print("[ERROR] Nvidia GPU status fetch error")
            return []
        
    @classmethod
    def get_gpu_status_amd(cls):
        try:
            outputs = subprocess.check_output(["rocm-smi", "--showproductname", "--showtemp", "--showmemuse", "--showuse"],universal_newlines=True)
            outputs = outputs.strip().splitlines()
            info = []
            for output in outputs:
                gpu = {}
                output = output.strip()
                if "Card series" in output:
                    gpu["model"] = output.split(":")[-1].strip()
                if "Temperature" in output:
                    temp = re.search(r"(\d+\.?\d*)", output)
                    if temp:
                        gpu["temperature"] = temp.group()
                if "Used VRAM" in output or "VRAM Usage" in output:
                    mem = re.search(r"(\d+)\s*MiB.*?\/\s*(\d+)\s*MiB", output)
                if mem:
                    gpu["vram_usage"] = f"{mem.group(1)} MiB"
                    gpu["vram_total"] = f"{mem.group(2)} MiB"
                if "GPU use" in output:
                    util = re.search(r"(\d+)\s*%", output)
                    if util:
                        gpu["usage"] = f"{util.group()} %"
                info.append(gpu)
            return info
        except Exception:
            return []
