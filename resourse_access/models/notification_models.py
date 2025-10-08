from sqlalchemy import BigInteger, Boolean, Column, Integer, Text, JSON, TIMESTAMP, CheckConstraint, ForeignKey
from sqlalchemy.sql import func
from resourse_access.db_base_class import Base
from schemas.enums import NotificationPriorityEnum
from schemas.enums import NotificationStatusEnum
from schemas.enums import NotificationPlatformEnum
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ENUM


class DeviceDB(Base):
    __tablename__ = "devices"
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    fcm_token = Column(Text, unique=True, nullable=False, index=True)
    platform = Column(ENUM(NotificationPlatformEnum), nullable=False)
    app_version = Column(String, nullable=True)
    locale = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    __table_args__ = (CheckConstraint("platform in ('android','ios','web')", name="ck_devices_platform"),)

class NotificationLogDB(Base):
    __tablename__ = "notification_logs"
    user_id = Column(BigInteger, index=True, nullable=True)
    title = Column(String, nullable=True)
    body = Column(Text, nullable=True)
    data = Column(JSON, nullable=True)
    priority = Column(ENUM(NotificationPriorityEnum), nullable=True)
    ttl_seconds = Column(Integer)
    status = Column(ENUM(NotificationStatusEnum), nullable=True)
    error = Column(Text, nullable=True)
    sent_at = Column(TIMESTAMP(timezone=True), nullable=True)
