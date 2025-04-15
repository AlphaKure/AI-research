import src.utils as utils 

from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title = utils.Project_Config.title,
    version= utils.Project_Config.version
)


if __name__ == "__main__":
    uvicorn.run(app,host=utils.Project_Config.ip,port=utils.Project_Config.port)

