from typing import Optional


excluded_fields_base = {
    "crAt": 0,
    "upAt": 0,
}


def make_excluded_fields(fields: Optional[list[str]] = None) -> dict[str, int]:
    exclude_fields = excluded_fields_base
    if fields is not None:
        extra = {field: 0 for field in fields}
        return {**exclude_fields, **extra}
    return exclude_fields
