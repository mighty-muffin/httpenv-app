from fastapi import FastAPI
import uvicorn
import os
from dotenv import load_dotenv


load_dotenv()

SECRET = os.getenv("SECRET", "123456")

app = FastAPI()


@app.get("/")
def hello(name: str = "World"):
    return f"Hello, {name}!"


@app.get("/bye")
def bye(name: str = "World"):
    return f"Goodbye, {name}!"


@app.get("/policeducode")
def police_ducode(name: str = "SECRET"):
    return f"The secret is... {SECRET}!"
