from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello from FastAPI on Kubernetes!"}

@app.get("/add/{a}/{b}")
def add(a: int, b: int):
    return {"result": a + b}
