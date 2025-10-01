
from resourse_access.db_base_class import Base
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy.dialects.postgresql import ENUM

from schemas.enums import GenderEnum, UserRoleEnum


class UserDB(Base):
    __tablename__ = 'users'

    privy_id = Column(String, unique=True, nullable=False, index=True)   
    phone_number = Column(String, unique=True)   
    email = Column(String, nullable=True)              
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(ENUM(UserRoleEnum), default='customer')
    gender = Column(ENUM(GenderEnum), default='other')
    
   #  wallets = relationship("Wallet", back_populates="user")
