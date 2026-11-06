from datetime import datetime, timezone

from sqlalchemy.orm import Session
from sqlalchemy import desc, select

from app.notifications.model.notification_status import NotificationStatus
from app.notifications.model.notification_orm import NotificationORM
from app.db.database import Base, engine


def create_tables():
    Base.metadata.create_all(engine)


def get_all_notifications(db: Session):
    query = (
        select(NotificationORM)
        .order_by(desc(NotificationORM.scheduled_at))
    )

    result = db.execute(query)
    return result.scalars().all()


def get_notification_by_id(db: Session, id: int):
    query = select(NotificationORM).where(NotificationORM.id == id)
    result = db.execute(query).scalars().all()

    try:
        return result[0]
    except:
        return None


def add_notification(db: Session, notification: NotificationORM):
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


def get_ready_notifications(db: Session) -> list[NotificationORM]:
    now_utc = datetime.now(timezone.utc)

    query = (
        select(NotificationORM)
        .where(NotificationORM.status == NotificationStatus.PENDING)
        .where(NotificationORM.scheduled_at <= now_utc)
        .order_by(NotificationORM.scheduled_at)
    )

    result = db.execute(query)

    return list(result.scalars().all())


def save_notification(db: Session, notification_data: NotificationORM):
    db.commit()
    db.refresh(notification_data)
    
    return notification_data


def count_notifications_by_status(db: Session, status_value: str) -> int:
    return (
        db.query(NotificationORM)
        .filter(NotificationORM.status == status_value)
        .count()
    )


def count_notifications_by_status_and_channel(
    db: Session,
    status_value: str,
    channel_value: str,
    ) -> int:
    return (
        db.query(NotificationORM)
        .filter(NotificationORM.status == status_value)
        .filter(NotificationORM.channel == channel_value)
        .count()
    )
