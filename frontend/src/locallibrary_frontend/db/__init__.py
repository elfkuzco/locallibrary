import subprocess
from collections.abc import Generator
from pathlib import Path

from sqlalchemy import SelectBase, create_engine, func, select
from sqlalchemy.orm import Session as OrmSession
from sqlalchemy.orm import sessionmaker

from locallibrary_frontend import logger
from locallibrary_frontend.settings import Settings

Session = sessionmaker(
    bind=create_engine(url=Settings.DATABASE_URL, echo=False),
    expire_on_commit=False,
)


def gen_dbsession() -> Generator[OrmSession, None, None]:
    """FastAPI's Depends() compatible helper to provide a begin DB Session"""
    with Session.begin() as session:
        yield session


def upgrade_db_schema():
    """Checks if Alembic schema has been applied to the DB"""
    src_dir = Path(__file__).parent.parent
    logger.info(f"Upgrading database schema with config in {src_dir}")
    subprocess.check_output(args=["alembic", "upgrade", "head"], cwd=src_dir)


def count_from_stmt(session: OrmSession, stmt: SelectBase) -> int:
    """Count all records returned by any statement `stmt` passed as parameter"""
    return session.execute(
        select(func.count()).select_from(stmt.subquery())
    ).scalar_one()
