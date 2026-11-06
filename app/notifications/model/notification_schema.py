from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.notifications.model.notification_status import NotificationStatus
from app.notifications.model.notification_channel import NotificationChannel


class NotificationCreate(BaseModel):
    content: str
    channel: NotificationChannel
    recipient: str
    scheduled_at: datetime
    timezone: str

    model_config = ConfigDict(from_attributes=True)


class NotificationResponse(BaseModel):
    id: int
    content: str
    channel: NotificationChannel
    recipient: str
    scheduled_at: datetime
    created_at: datetime
    timezone: str
    status: NotificationStatus
    idempotency_key: str

    model_config = ConfigDict(from_attributes=True)
