from db import db
from typing import List
from models.addresses import AddressModel

class OrganizationModel(db.Model):
    __tablename__ = "organization"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    addresses = db.relationship("AddressModel", lazy="dynamic")


    @classmethod
    def find_by_name(cls, name: str) -> "OrganizationModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["OrganizationModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
