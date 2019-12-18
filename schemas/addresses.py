from ma import ma
from models.addresses import AddressModel



class AddressSchema(ma.ModelSchema):
    class Meta:
        model = AddressModel
        dump_only = ("id",)

        include_fk = True
