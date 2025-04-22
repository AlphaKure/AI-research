from src.utils.system import System

import os
import sys
import re
import shutil
import subprocess

import clr

class CPU:

    is_ready : bool = False # For Windows

    @classmethod
    def libre_hardware_monitor_setup(cls):
        DLLPATH = System.root.parent / "tools" / "LibreHardwareMonitor"/ "LibreHardwareMonitorLib.dll"
        if not os.path.isfile(str(DLLPATH)):
            print("[WARNING] You didn't setup LibreHardwareMonitor")
        else:
            clr.AddReference(str(DLLPATH))
            from LibreHardwareMonitor import Hardware # 讀取DLL內容
            cls._terminal = Hardware.Computer()
            cls._terminal.IsCpuEnabled = True
            cls._terminal.Open()
            cls.is_ready = True

    @classmethod
    def get_cpu_status(cls):
        if System.operating_system == "Windows":
            if not cls.is_ready:
                cls.libre_hardware_monitor_setup()
            return cls.get_cpu_status_windows()
        elif System.operating_system == "Linux":
            return cls.get_cpu_status_linux()
        else:
            print("[ERROR] Operating System error")
            sys.exit()
    
    @classmethod
    def get_cpu_status_windows(cls):
        
        datas = []
        for hardware in cls._terminal.Hardware:
            hardware.Update()

            usage = 0.0
            temperature = 0.0
            for sensor in hardware.Sensors:
                if str(sensor.SensorType) == "Temperature" and sensor.Name == "Core Average":
                    temperature = sensor.Value
                elif str(sensor.SensorType) == "Load" and sensor.Name == "CPU Total":
                    usage = sensor.Value
            
            datas.append({
                "name": hardware.Name,
                "temperature": temperature,
                "usage": usage
            })

        return datas

    @classmethod
    def get_cpu_status_linux(cls):

        import cpuinfo
        import psutil
        cpuName = cpuinfo.get_cpu_info().get("brand_raw", "Unknown CPU") 
        cpuUsage = round(psutil.cpu_percent(interval=1), 1) 
        cpuTemp = 0.0
        if shutil.which("sensors"):
            lm_sensor_output = subprocess.check_output(["sensors"], text=True)
            match = re.findall(r"Package id \d+:\s+\+?([\d.]+)", lm_sensor_output)
            if match:
                cpuTemp = max(map(float, match))
        return [{"name":cpuName, "temperature": cpuTemp , "usage":cpuUsage}]