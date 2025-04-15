from src.utils.system import System

from configparser import ConfigParser

ini_path = System.root / "utils" / "config" / "project.ini"
reader =  ConfigParser()
reader.read(ini_path)

class Project_Config:
    
    # Fastapi
    version : str = reader["fastapi"]["version"]
    title : str = reader["fastapi"]["title"]

    ip : str = reader["system"]["ip"]
    port : int = int(reader["system"]["port"])
    