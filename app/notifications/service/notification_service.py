import secrets

from typing import Optional

from sqlalchemy.orm import Session

from app.notifications.data.notification_repository import add_notification, get_all_notifications, save_notification
from app.notifications.model.notification_channel import NotificationChannel
from app.notifications.model.notification_schema import NotificationCreate
from app.notifications.model.notification_status import NotificationStatus
from app.notifications.model.notification_orm import NotificationORM
from app.notifications.service.notification_dispatcher import dispatch_notification
from app.notifications.service.notification_validation import validate_content, validate_notification_exists_id, validate_recipient, validate_timezone, validate_scheduled_at, convert_to_utc


def generate_idempotency_key() -> str:
    return f"notif_{secrets.token_urlsafe(24)}"


def list_notifications(db: Session, id: Optional[int]=None):
    return validate_notification_exists_id(db, id) if id else get_all_notifications(db)


def create_notification(db: Session, notification_data: NotificationCreate) -> NotificationORM:
    validate_content(notification_data.content)
    validate_timezone(notification_data.timezone)
    validate_scheduled_at(notification_data.scheduled_at, notification_data.timezone)

    if notification_data.channel == NotificationChannel.EMAIL:
        validate_recipient(notification_data.recipient)

    scheduled_at_utc = convert_to_utc(
        notification_data.scheduled_at,
        notification_data.timezone,
    )

    notification = NotificationORM(
        content=notification_data.content,
        channel=notification_data.channel,
        recipient=notification_data.recipient,
        scheduled_at=scheduled_at_utc,
        timezone=notification_data.timezone,
        status=NotificationStatus.PENDING,
        idempotency_key=generate_idempotency_key(),
    )

    return add_notification(db, notification)


def execute_notification(db: Session, notification_id: int) -> NotificationORM:
    notification = validate_notification_exists_id(db, notification_id)
    
    current_status = notification.status

    if current_status != NotificationStatus.PENDING:
        raise ValueError("Wykonać można wyłącznie powiadomienie w statusie PENDING.")

    try:
        dispatch_notification(notification)

        notification.status = NotificationStatus.SENT
    except Exception as exc:
        print(f"[DEBUG] Delivery failed: {repr(exc)}")
        notification.status = NotificationStatus.FAILED

    return save_notification(db, notification)
