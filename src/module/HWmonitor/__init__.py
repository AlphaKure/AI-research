from src.module.HWmonitor.cpu import CPU

import asyncio
import json
from typing import Union

from fastapi import WebSocket

class HardWareDashBoard:

    is_hardware_dashboard_running = False
    
    websocket : Union[WebSocket, None] = None
    tasks : dict[str,asyncio.Task] = {}

    @classmethod
    def request_process(cls,websocket: WebSocket, request):
        if request.get("type").lower() == "hardware_dataflow":
            
            if request.get("enable") == True and not cls.is_hardware_dashboard_running:
                cls.websocket = websocket
                cls.start_hardware_dataflow(request.get("frequency"))
            elif request.get("enable") == False and cls.is_hardware_dashboard_running:
                cls.end_hardware_dataflow()
        else:
            return       
    
    @classmethod
    def start_hardware_dataflow(cls, freq):
        cls.is_hardware_dashboard_running = True
        cls.tasks["hardware_dataflow"]=asyncio.create_task(cls.loop_get_cpu_status(freq))

    @classmethod
    def end_hardware_dataflow(cls):
        cls.is_hardware_dashboard_running = False
        if cls.tasks["hardware_dataflow"] and not cls.tasks["hardware_dataflow"].done():
            cls.tasks["hardware_dataflow"].cancel()
            del cls.tasks["hardware_dataflow"]
    
    @classmethod
    async def loop_get_cpu_status(cls,freq: int = 1):
        try:
            while cls.is_hardware_dashboard_running:
                data = await asyncio.to_thread(CPU.get_cpu_status)
                if cls.websocket:
                    await cls.websocket.send_text(json.dumps(data))
                await asyncio.sleep(freq)
        except asyncio.CancelledError:
            pass