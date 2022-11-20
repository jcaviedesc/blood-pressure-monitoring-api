from ...core.baseModel import DatetimeModelMixin, IDModelMixin

# TODO arreglar para que DatatimeModelMixin no sobreescriba los valores que trae la base de datos
class DeviceModel(IDModelMixin, DatetimeModelMixin):
    user_id: str
    token: str
