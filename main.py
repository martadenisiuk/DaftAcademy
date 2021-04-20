from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello world!"}

@app.api_route(path="/method", methods=["DELETE"])
def read_request(request: Request):
    return {"method": request.method}
