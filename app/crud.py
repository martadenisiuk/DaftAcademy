from sqlalchemy.orm import Session
from sqlalchemy import update

from . import models, schemas


def get_shippers(db: Session):
    return db.query(models.Shipper).all()


def get_shipper(db: Session, shipper_id: int):
    return (
        db.query(models.Shipper).filter(models.Shipper.ShipperID == shipper_id).first()
    )

def get_suppliers(db: Session):
    return db.query(models.Supplier).all()


def get_supplier(db: Session, id: int):
    return (
        db.query(models.Supplier).filter(models.Supplier.SupplierID == id).first()
    )


def get_product(db: Session, id: int):
    return (
    db.query(models.Product.ProductID,
                    models.Product.ProductName,
                    models.Category.CategoryID,
                    models.Category.CategoryName,
                    models.Product.Discontinued,
                    ).
        join(models.Category, models.Product.CategoryID == models.Category.CategoryID).
        filter(models.Product.SupplierID == id).
        order_by(models.Product.ProductID.desc()).all()
        )


def create_supplier(db: Session, supplier: schemas.Add_Supplier):
    id = db.query(models.Supplier).count() + 1
    db_supplier = models.Supplier(
        SupplierID = id,
        CompanyName = supplier.CompanyName,
        ContactName = supplier.ContactName,
        ContactTitle = supplier.ContactTitle,
        Address = supplier.Address,
        City = supplier.City,
        PostalCode = supplier.PostalCode,
        Country = supplier.Country,
        Phone = supplier.Phone
    )
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier
    pass



def put_supplier(db:Session, id : int, supplier: schemas.PutSupplier):
    put_supplier = {col: val for col, val in dict(supplier).items() if val is not 'string'}
    if put_supplier:
        db.query(models.Supplier).filter(models.Supplier.SupplierID == id).update(values=put_supplier)
        db.commit()
        pass
