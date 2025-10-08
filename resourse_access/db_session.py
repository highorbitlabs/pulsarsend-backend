from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from supabase import create_client

from core.config import get_app_settings

settings = get_app_settings()

async_engine = create_async_engine(settings.get_async_database_url())

async_engine = create_async_engine(
    settings.get_async_database_url(),
    pool_pre_ping=True,                 
    pool_recycle=300,                   
    max_overflow=0,                     
    pool_size=5,                        
    connect_args={"statement_cache_size": 0},
)

AsyncSessionLocal = sessionmaker(
    bind=async_engine, expire_on_commit=False, class_=AsyncSession
)

sync_engine = create_engine(settings.get_database_url())
SessionLocal = sessionmaker(bind=sync_engine, expire_on_commit=False, class_=Session)
