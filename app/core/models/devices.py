from ...core.baseModel import DatatimeModelMixin, IDModelMixin

# TODO arreglar para que DatatimeModelMixin no sobreescriba los valores que trae la base de datos
class DeviceModel(IDModelMixin, DatatimeModelMixin):
    user_id: str
    token: str
