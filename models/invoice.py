from db import db
import datetime
from typing import List

from models.organization import OrganizationModel
from models.items import ItemsModel
from sqlalchemy import func


class InvoiceModel(db.Model):
    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True)
    ref_number = db.Column(db.String(10), nullable=False)

    org_id = db.Column(db.Integer, db.ForeignKey("organization.id"), nullable=True)

    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.datetime.now())

    # items_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False)
    items = db.relationship("ItemsModel", lazy="dynamic")

    amount = db.Column(db.Float, nullable=False)

    @classmethod
    def find_by_ref(cls, ref_number: int) -> "InvoiceModel":
        return cls.query.filter_by(ref_number=ref_number).first()

    @classmethod
    def find_by_id(cls, id: int) -> "InvoiceModel":
        return cls.query.filter_by(id=id).first()

    def calc_sum(self):
        return (item.price * self.amount for item in self.items)




    @classmethod
    def find_all(cls) -> List["InvoiceModel"]:
        return cls.query.all()


    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
