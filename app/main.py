from fastapi import FastAPI
import uvicorn
import os
from dotenv import load_dotenv


load_dotenv()

SECRET = os.getenv("SECRET", "123456")
FEATURE_GOODBYE = os.getenv("FEATURE_GOODBYE", False)

app = FastAPI()


@app.get("/")
def hello(name: str = "World"):
    return f"Hello, {name}!"


if FEATURE_GOODBYE:

    @app.get("/goodbye")
    def goodbye(name: str = "World"):
        return f"Goodbye, {name}!"


@app.get("/policeducode")
def police_ducode(name: str = "SECRET"):
    return f"The secret is... {SECRET}!"


if __name__ == "__main__":
    uvicorn.run(app, port=8080)
