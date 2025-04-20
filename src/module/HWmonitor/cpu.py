from src.utils.system import System

import os
import sys

import clr

class CPU:

    is_ready : bool = False # For LHM

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
            pass # TODO
        else:
            print("[ERROR] Operating System error")
            sys.exit(-1)
    
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