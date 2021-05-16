from sqlalchemy.orm import Session

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
        db.query(models.Product.ProductID, models.Product.ProductName,
                    models.Category.CategoryID, models.Category.CategoryName, 
                 models.Product.Discontinued).
        join(models.Category, models.Category.CategoryID == models.Product.CategoryID).
        filter(models.Product.SupplierID == id).
        order_by(models.Product.ProductID.desc()).all()
    )
