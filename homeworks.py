from fastapi import FastAPI
app = FastAPI()
import sqlite3

@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect("northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific 


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()
    
    
@app.get("/categories")
async def categories():
    app.db_connection.row_factory = sqlite3.Row
    categories = app.db_connection.execute('''SELECT CategoryID, CategoryName FROM Categories ORDER BY CategoryID''')\
    .fetchall()
    return {
        "categories": [{'id': f"{x['CategoryID']}", 'name':f"{x['CategoryName']}"} for x in categories]
    }

@app.get("/customers")
async def products():
    app.db_connection.row_factory = sqlite3.Row
    customers = app.db_connection.execute('''SELECT CustomerID, CompanyName, Address || ' ' ||
                                          COALESCE(PostalCode, '')|| ' ' || City || ' ' || Country 
                                          AS address FROM Customers ORDER BY UPPER(CustomerID)''').fetchall()
    return {
        "customers": [{'id': f"{x['CustomerID']}", 'name' : f"{x['CompanyName']}", 'full_address': f"{x['address']}"}  
                      for x in customers]
    }
