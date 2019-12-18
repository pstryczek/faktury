from db import db
from typing import List


class AddressModel(db.Model):
    __tablename__ = "addresses"
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.String(6), nullable=False)
    # organization_id = db.Column(
    #     db.Integer, db.ForeignKey("organization.id"), nullable=False
    # )

    @classmethod
    def find_by_name(cls, address: str) -> "AddressModel":
        return cls.query.filter_by(address=address).first()

    @classmethod
    def find_by_city(cls, city: str) -> "AddressModel":
        return cls.query.filter_by(city=city).first()

    @classmethod
    def find_all(cls) -> List["AddressModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
