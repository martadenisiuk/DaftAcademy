from fastapi import FastAPI, Request, Response, status, HTTPException, Depends, Cookie
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse
from pydantic import BaseModel
import hashlib
import re
import secrets

from fastapi.security import HTTPBasic, HTTPBasicCredentials
  
from typing import Dict
from datetime import date, timedelta

from fastapi.templating import Jinja2Templates

class Patient(BaseModel):
    name: str
    surname: str

app = FastAPI()
app.counter: int = 1
app.storage: Dict[int, Patient] = {}
app.session_token = []
app.token = []

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
      

      
#### Lekcja 3 #####  

@app.get("/hello")
def hello():
    today_date = date.today().isoformat()
    content = "<h1>Hello! Today date is {}</h1>".format(today_date)
    return HTMLResponse(content=content)

security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.post("/login_session",status_code = 201)
def read_current_session(response : Response, username : str = Depends(get_current_username)):
    token = secrets.token_hex(32)
    app.session_token.append(token)
    response.set_cookie(key="session_token", value = token)
    return {"username": username}

@app.post("/login_token", status_code = 201)
def read_current_token(response: Response,username: str = Depends(get_current_username)):
    token = secrets.token_hex(32)
    app.token.append(token)
    return {"token" : token}
  
@app.get('/welcome_session')
def welcome_session(response : Response, session_token = Cookie(None), format : str = ''):
    if session_token not in app.session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    if format == 'json':
        return JSONResponse(content={"message": "Welcome!"})
    elif format == 'html':
        content = '<h1>Welcome!</h1>'
        return HTMLResponse(content = content)
    else:
        return PlainTextResponse('Welcome!')

@app.get('/welcome_token')
def welcome_token(response : Response, token : str = '', format : str = ''):
    if token not in app.token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    if format == 'json':
        return JSONResponse(content={"message": "Welcome!"})
    elif format == 'html':
        content = '<h1>Welcome!</h1>'
        return HTMLResponse(content = content)
    else:
        return PlainTextResponse('Welcome!')
