from datetime import datetime, timezone
import re
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from sqlalchemy.orm import Session

from app.notifications.data.notification_repository import get_notification_by_id


class ValidationError(Exception):
    pass

class ConflictError(Exception):
    pass

class ResourceNotFoundError(Exception):
    pass


def validate_timezone(timezone_name: str):
    if not timezone_name or not timezone_name.strip():
        raise ValidationError("Strefa czasowa jest wymagana.")

    try:
        ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError as exc:
        raise ValidationError("Podana strefa czasowa jest nieprawidłowa.") from exc


def convert_to_utc(scheduled_at: datetime, timezone_name: str) -> datetime:
    """
    Przyjmuje datę planowanej wysyłki oraz nazwę strefy czasowej.
    Zwraca datę przekonwertowaną do UTC.
    """
    zone = ZoneInfo(timezone_name)

    if scheduled_at.tzinfo is None:
        local_dt = scheduled_at.replace(tzinfo=zone)
    else:
        local_dt = scheduled_at.astimezone(zone)

    return local_dt.astimezone(timezone.utc)


def validate_scheduled_at(scheduled_at: datetime, timezone_name: str):
    scheduled_at_utc = convert_to_utc(scheduled_at, timezone_name)

    if scheduled_at_utc <= datetime.now(timezone.utc):
        raise ValidationError("Planowana data wysyłki musi wskazywać przyszły moment.")


def validate_content(content: str):
    pass


def validate_notification_exists_id(db: Session, id: int):
    notification = get_notification_by_id(db, id)

    if not notification:
        raise ResourceNotFoundError("Nie ma powiadomienia o takim ID.")

    return notification


def validate_recipient(recipient: str):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", recipient):
        raise ValidationError("Błędny adres e-mail.")

    return recipient
