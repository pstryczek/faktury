from ma import ma
from models.invoice import InvoiceModel
from schemas.items import ItemsSchema
from schemas.organization import OrganizationSchema


class InvoiceSchema(ma.ModelSchema):
    items = ma.Nested(ItemsSchema, many=True)
    organization = ma.Nested(OrganizationSchema, many=True)

    class Meta:
        model = InvoiceModel
        dump_only = ("id", "created_by", "created_at",)
        include_fk = True
