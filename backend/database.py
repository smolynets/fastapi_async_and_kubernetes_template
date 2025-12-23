import asyncio
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from backend import config


# ==================== POSTGRES ====================

# POSTGRES_USER = os.getenv("POSTGRES_USER", "psql_user")
# POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "psql_password")
# POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")  # k8s: postgres, docker-compose: db
# POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
# DATABASE = os.getenv("DATABASE", "postgres")

# POSTGRES_PORT = str(POSTGRES_PORT).replace("tcp:", "")

# DATABASE_URL = (
#    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
#    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{DATABASE}"
# )

DATABASE_URL = f"postgresql+asyncpg://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_HOST}:5432/{config.DATABASE}"

engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# ==================== REDIS ====================

# async def get_redis_client() -> Redis:
#     redis_client = Redis(host=config.REDIS_HOST, 
#                          port=config.REDIS_PORT, 
#                          db=0)
#     return redis_client

if __name__ == "__main__":
    asyncio.run(init_models())
