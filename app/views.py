from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from . import crud, schemas, models
from .database import get_db

router = APIRouter()


@router.get("/shippers/{shipper_id}", response_model=schemas.Shipper)
async def get_shipper(shipper_id: PositiveInt, db: Session = Depends(get_db)):
    db_shipper = crud.get_shipper(db, shipper_id)
    if db_shipper is None:
        raise HTTPException(status_code=404, detail="Shipper not found")
    return db_shipper


@router.get("/shippers", response_model=List[schemas.Shipper])
async def get_shippers(db: Session = Depends(get_db)):
    return crud.get_shippers(db)


@router.get("/suppliers/{id}", response_model=schemas.Suppliers)
async def get_suppliers(id: PositiveInt, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier


@router.get("/suppliers", response_model=List[schemas.Supplier])
async def get_supplier(db: Session = Depends(get_db)):
    return crud.get_suppliers(db)



@router.get('/suppliers/{id}/products')
async def get_products(id: PositiveInt, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    db_products = crud.get_product(db, id)        
    return [{
        'ProductID' : product.ProductID,
        'ProductName' : product.ProductName,
        'Category' : {
            'CategoryID' : product.CategoryID,
            'CategoryName' : product.CategoryName},
        'Discontinued' : product.Discontinued}
        for product in db_products]


@router.post("/suppliers", response_model=schemas.ResSupplier, status_code=201)
async def create_supplier(supplier: schemas.Add_Supplier, db: Session = Depends(get_db)):
    return crud.create_supplier(db, supplier)




@router.put('/suppliers{id}', response_model=schemas.PutSupplier, status_code=200)
async def put_supplier(id:PositiveInt,supplier: schemas.PutSupplier, db: Session = Depends(get_db)):
    if crud.get_supplier(db, id) is None:
        raise HTTPException(status_code=401, detail="Supplier not found")    
    crud.modify_suppliers(db, id, supplier)
    return crud.get_supplier(db, id)


