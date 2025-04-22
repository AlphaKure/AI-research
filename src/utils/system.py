from pathlib import Path
import platform
import subprocess
import sys
from typing import ClassVar,Literal

class System:

    root : ClassVar[Path] = Path(__file__).resolve().parent.parent # point to src

    operating_system: ClassVar[Literal["Windows","Linux"]] = platform.system()
    
    @staticmethod
    def identify_device(devices: list[str]) :
        if len(devices) == 0:
            sys.exit()
        else:
            for device in devices:
                device = device.lower()
                if  "intel" in device or "apu" in device or "uhd" in device:
                    continue # 跳過內顯
                elif "nvidia" in device:
                    return "nvidia"
                elif "amd" in device or "radeon" in device:
                    return "amd"
                else:
                    return "unknown"
            return "unknown"

    @classmethod
    def get_gpu_type(cls):
        if cls.operating_system == "Windows":
            try:
                command_outputs = subprocess.check_output(["wmic", "path", "win32_VideoController", "get", "Name"], universal_newlines=True)
                devices = command_outputs.strip().split("\n")[2:] # 純文字轉list 並移除標題及空行
                return cls.identify_device(devices)
            except:
                print("[Error] Can not get gpu type")
                sys.exit()
        elif cls.operating_system == "Linux":
            try:
                command_outputs = subprocess.check_output(["lspci"], universal_newlines=True).split("\n")
                devices = []
                for output in command_outputs:
                    if 'VGA compatible controller' in output or '3D controller' in output:
                        devices.append(output)
                return cls.identify_device(devices)
            except:
                print("[Error] Can not get gpu type")
                sys.exit()
        else:
            print("[WARNING] Not support on this operating system")
            sys.exit()
    
    @classmethod
    def get_os_info(cls):
        return {"operating_system":cls.operating_system ,"gpu_type":cls.get_gpu_type()}