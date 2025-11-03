import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from src.core import settings

# SQLAlchemy 로깅 설정 수정
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
# 중복 로깅 방지를 위해 propagate 설정 비활성화
logging.getLogger("sqlalchemy.engine").propagate = False

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_pre_ping=True,  # 연결 사용 전 ping으로 유효성 검사
    future=True,          # 2.0 스타일
)

async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
  async with async_session() as db:
    yield db