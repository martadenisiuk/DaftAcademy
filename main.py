from fastapi import FastAPI, Request, Response, status
from pydantic import BaseModel
import hashlib
import re
  
from typing import Dict
from datetime import date, timedelta

from fastapi.templating import Jinja2Templates


class Patient(BaseModel):
    name: str
    surname: str

app = FastAPI()
app.counter: int = 1
app.storage: Dict[int, Patient] = {}

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
    len_string = len(''.join(filter(str.isalpha, patient.name + patient.surname)))
    #len_string = len(re.sub('[^A-Za-z]+', '', patient.name + patient.surname))
    resp = {"id": app.counter, "name": patient.name, "surname": patient.surname,
            "register_date" : date.today(), "vaccination_date" : date.today() + timedelta(len_string)}
    app.storage[app.counter] = resp
    app.counter += 1
    return resp

@app.get("/patient/{id}")
def show_patient(id : int):
    if id in app.storage:
        return app.storage.get(id)
    elif id < 1: 
        return Response(status_code = 400)
    else:
        return Response(status_code = 404)
      
#### Lekcja 3 #####  

templates = Jinja2Templates(directory="templates")
@app.get("/jinja")
def read_item(request: Request):
    return templates.TemplateResponse("index.html.j2", {
        "request": request, "my_string": "Wheeeee!", "my_list": [0, 1, 2, 3, 4, 5]})

