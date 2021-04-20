from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
import hashlib

app = FastAPI()

class User(BaseModel):
    password: str
    password_hash: str

@app.get("/")
def root():
    return {"message": "Hello world!"}

@app.api_route(path="/method", methods=["GET", "DELETE", "PUT", "OPTIONS"])
def read_request(request: Request):
    return {"method": request.method}

@app.api_route(path = '/method', methods=["POST"], status_code=201)
def read_request(request: Request):
    return {"method": request.method}

@app.get("/auth")
def auth(password: str = '', password_hash: str = ''):
    try:
        h = hashlib.sha512(bytes(password, encoding="ASCII"))
        if password == '' or password_hash == '':
            status_code = 401
        elif str(h.hexdigest()) == password_hash:
            status_code = 204
        else:
            status_code = 401
    except Exception:
        status_code = 401
    return Response(status_code=status_code)
