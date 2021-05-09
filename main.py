from fastapi import FastAPI, HTTPException, Response
import uvicorn
import sqlite3

from typing import Optional

app = FastAPI()

with sqlite3.connect("northwind.db") as connection:
    connection.text_factory = lambda b: b.decode(errors="ignore")
    cursor = connection.cursor()
    products = cursor.execute("SELECT ProductName FROM Products").fetchall()
    print(len(products))
    print(products[4])

@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect("northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific 


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()
    
    
###### Zadanie 1 ##########
    
@app.get("/categories")
async def categories():
    app.db_connection.row_factory = sqlite3.Row
    categories = app.db_connection.execute('SELECT CategoryID, CategoryName FROM Categories ORDER BY CategoryID').fetchall()
    return {
        "categories": [{'id': f"{x['CategoryID']}", 'name':f"{x['CategoryName']}"} for x in categories]
    }

@app.get("/customers")
async def customers():
    app.db_connection.row_factory = sqlite3.Row
    customers = app.db_connection.execute('''SELECT CustomerID, CompanyName, COALESCE(Address, '') || ' ' ||
                                          COALESCE(PostalCode, '')|| ' ' || COALESCE(City,'') || ' ' || COALESCE(Country,'') 
                                          AS address FROM Customers ORDER BY UPPER(CustomerID)''').fetchall()
    return {
        "customers": [{'id': f"{x['CustomerID']}", 'name' : f"{x['CompanyName']}", 'full_address': f"{x['address']}"}  
                      for x in customers]
    }


###### Zadanie 2 ##########
'''
@app.get('/products/{id}')
async def  products(id : int):
    app.db_connection.row_factory = sqlite3.Row
    try:
        products = app.db_connection.execute(f"SELECT ProductID id, ProductName name FROM Products WHERE id = {id}" ).fetchone()
        return products
    except Exception:
        status_code = 404
        return Response(status_code=status_code)
                      
@app.get('/products/{id}')
async def  products(id : int):
    app.db_connection.row_factory = sqlite3.Row
    products = app.db_connection.execute(f"SELECT ProductID id, ProductName name FROM Products WHERE id = {id}" ).fetchone()
    if products is not None:
        return products
    else:
        raise HTTPException(status_code=404) '''
                      
@app.get('/products/{id}')
async def  products(id : int):
    try:
        app.db_connection.row_factory = sqlite3.Row
        products = app.db_connection.execute(f'''SELECT ProductID id, ProductName name FROM Products WHERE id = {id}''' ).fetchone()
        if products is not None:
            Response(status_code = 200)
            return products
        else:
            raise HTTPException(status_code = 404)
    except Exception:
        raise HTTPException(status_code=404)                      
                      
###### Zadanie 3 ##########
variables = {'id', 'first_name', 'last_name', 'city'}

@app.get('/employees')
async def employees(limit : Optional[int] = -1, offset : Optional[int] = 0, order : Optional[str] = 'id'):
    if order not in variables:
        raise HTTPException(status_code = 400)
    app.db_connection.row_factory = sqlite3.Row
    employees = app.db_connection.execute(f'SELECT EmployeeID id, LastName last_name, FirstName first_name,\
                                          City city FROM Employees ORDER BY {order} LIMIT {limit} OFFSET {offset}').fetchall()
    return {'employees' : employees}                
                     
###### Zadanie 4 ########

@app.get('/products_extended')
async def products_extended():
    app.db_connection.row_factory = sqlite3.Row
    products_extended = app.db_connection.execute('''SELECT Products.ProductID id, Products.ProductName name, 
                                                  Categories.CategoryName category, Suppliers.CompanyName supplier 
                                                  FROM ((Products INNER JOIN Categories ON Categories.CategoryID = 
                                                         Products.CategoryID) INNER JOIN Suppliers ON 
                                                        Suppliers.SupplierID = Products.SupplierID)''').fetchall()                     
