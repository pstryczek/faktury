from ma import ma
from models.items import ItemsModel
from models.invoice import InvoiceModel


class ItemsSchema(ma.ModelSchema):
    class Meta:
        model = ItemsModel
        dump_only = ("id",)
        # dump_only = ("id",)
        include_fk = True
