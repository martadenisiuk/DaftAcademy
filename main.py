from fastapi import FastAPI, Request, Response, status
from pydantic import BaseModel
import hashlib
import re
  
from datetime import date, timedelta

class Patient(BaseModel):
    name: str
    surname: str

app = FastAPI()
app.counter: int = 0

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

@app.post("/register", status_code = 201)
def show_data(patient: Patient):
    len_string = len(re.sub('[^A-Za-z]+', '', patient.name + patient.surname))
    resp = {"id": app.counter, "name": patient.name, "surname": patient.surname,
            "register_date" : date.today(), "vaccination_date" : date.today() + timedelta(len_string)}
    #app.storage[app.counter] = patient
    app.counter += 1
    return resp
