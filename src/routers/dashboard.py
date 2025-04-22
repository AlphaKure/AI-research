from src.module.HWmonitor import HardWareDashBoard

from fastapi import APIRouter, WebSocketDisconnect, WebSocket 

route = APIRouter(
    tags=["Dashboard"]
)

@route.websocket("/dashboard")
async def dashboard(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            try:
                request = await ws.receive_json()
                HardWareDashBoard.request_process(ws,request)
            except:
                pass # 忽略前端JSON格式錯誤
    except WebSocketDisconnect:
        HardWareDashBoard.end_hardware_dataflow()