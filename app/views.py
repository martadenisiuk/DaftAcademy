from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import get_db

import requests

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

'''
@router.get('/suppliers/{id}/products')
async def get_products(id: PositiveInt, db: Session = Depends(get_db)):
    db_products = crud.get_product(db, id)
    if db_products is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return [{
        'ProductID' : product.ProductID,
        'ProductName' : product.ProductName,
        'Category' : {
            'CategoryID' : product.CategoryID,
            'CategoryName' : product.CategoryName},
        'Discontinued' : product.Discontinued}
        for product in db_products]'''

@router.get('/suppliers/{id}/products')
async def get_products(response:Response, id: PositiveInt, db: Session = Depends(get_db)):
    db_products = crud.get_product(db, id)
    try:
        data = [{
            'ProductID' : product.ProductID,
            'ProductName' : product.ProductName,
            'Category' : {
                'CategoryID' : product.CategoryID,
                'CategoryName' : product.CategoryName},
            'Discontinued' : product.Discontinued}
            for product in db_products]
            response.raise_for_status()
        return len(data)
    requests.exceptions.HTTPError:
        raise HTTPException(status_code = 404, detail='Supplier not found')
        




