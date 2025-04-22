import src.utils as utils 
import src.routers as routers

from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title = utils.Project_Config.title,
    version= utils.Project_Config.version
)

app.include_router(routers.system_route)
app.include_router(routers.dashboard_route)

if __name__ == "__main__":
    uvicorn.run(app,host=utils.Project_Config.ip,port=utils.Project_Config.port)

