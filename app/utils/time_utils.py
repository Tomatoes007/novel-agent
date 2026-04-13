from datetime import datetime


def utcnow_iso() -> str:
    return datetime.utcnow().isoformat()
