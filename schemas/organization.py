from ma import ma
from models.organization import OrganizationModel


class OrganizationSchema(ma.ModelSchema):
    class Meta:
        model = OrganizationModel
        load_only = ("organization",)
        dump_only = ("id",)
        include_fk = True
