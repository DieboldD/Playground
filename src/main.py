import os

from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def hello_world():
    name = os.environ.get("NAME", "World")
    return "Hello CICD {}!".format(name)


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=int(os.environ.get("PORT", 8080)))