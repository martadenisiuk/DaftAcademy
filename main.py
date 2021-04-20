from fastapi import FastAPI

app = FastAPI()

@app.get("/method")
def root():
    return {"method": "GET"}
