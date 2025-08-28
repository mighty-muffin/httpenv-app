import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

SECRET = os.getenv('SECRET', '123456')
FEATURE_FORMAL = os.getenv('FEATURE_FORMAL', True)
FEATURE_GOODBYE = os.getenv('FEATURE_GOODBYE', True)

app = FastAPI()

if FEATURE_FORMAL:

    @app.get('/')
    def hello_formal(name: str = 'World', formal: bool = False):
        if formal:
            return f'Good day to you, {name}.'
        return f'Hello, {name}!'

else:

    @app.get('/')
    def hello(name: str = 'World'):
        return f'Hello, {name}!'


if FEATURE_GOODBYE:

    @app.get('/goodbye')
    def goodbye(name: str = 'World'):
        return f'Goodbye, {name}!'


@app.get('/policeducode')
def police_ducode(name: str = 'SECRET'):
    return f'The secret is... {SECRET}!'


if __name__ == '__main__':
    uvicorn.run(app, port=8080)
