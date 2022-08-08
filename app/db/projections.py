from typing import Optional


excluded_fields_base = {
    "crAt": 0,
    "upAt": 0,
}


def make_excluded_fields(fields: Optional[list[str]] = None) -> dict[str, int]:
    excluede_fields = excluded_fields_base
    if fields is not None:
        extra = {field: 0 for field in fields}
        return {**excluede_fields, **extra}
    return excluede_fields
