from datetime import datetime

from sqlalchemy import DateTime, Enum, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.notifications.model.notification_status import NotificationStatus
from app.notifications.model.notification_channel import NotificationChannel


class NotificationORM(Base):
    __tablename__ = "notification"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(String)
    channel: Mapped[NotificationChannel] = mapped_column(Enum(
        NotificationChannel,
        name="notification_channel",
        create_constraint=True,
        validate_strings=True,
    ))
    recipient: Mapped[str] = mapped_column(String)
    scheduled_at: Mapped[datetime] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    timezone: Mapped[str] = mapped_column(String)
    status: Mapped[NotificationStatus] = mapped_column(Enum(
        NotificationStatus,
        name="notification_status",
        create_constraint=True,
        validate_strings=True,
    ))
    idempotency_key: Mapped[str] = mapped_column(String, nullable=False)
