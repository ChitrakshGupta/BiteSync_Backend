from datetime import datetime, timezone

from bson import ObjectId


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def str_object_id(value: ObjectId) -> str:
    return str(value)
