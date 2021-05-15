import os
import uvicorn
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def hello_world():
    name = os.environ.get("NAME", "World")
    return "Hello CICD {}!".format(name)


if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)