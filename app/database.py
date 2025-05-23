from sqlalchemy import create_engine, MetaData, Engine
from sqlalchemy.orm import sessionmaker
from app.config.settings import Settings
from app.config.logger import get_logger
import subprocess

engine: Engine | None = None
SessionLocal: sessionmaker | None = None
logger = get_logger(__name__, log_level='DEBUG')


def init_database(settings: Settings):
    database_url = make_database_url(settings)
    info_message = f'''
    Initializing database with:
        DATABASE_NAME: %s
        DATABASE_USERNAME: %s
        DATABASE_HOST: %s
        DATABASE_PORT: %s
        DATABASE_PASSWORD: [NOT SHOWN]
    '''
    logger.info(info_message,
                settings.database_name,
                settings.database_username,
                settings.database_host,
                settings.database_port)

    # Ensure DB tables are created (for development/demo only)
    # Normally would use a schema migration tool such as migrate or alembic
    try:
        global engine
        engine = create_engine(database_url)
        global SessionLocal
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        metadata = MetaData()
        metadata.reflect(bind=engine)
        logger.debug('All tables: %s', metadata.tables.keys())
    except Exception as e:
        logger.error(e)


def run_pyway_migrations(settings: Settings):
    logger.info("Running Pyway migrations:")
    result = subprocess.run(
        [
            "pyway",
            "migrate",
            f"--database-type=postgres",
            f"--database-username={settings.database_username}",
            f"--database-password={settings.database_password}",
            f"--database-host={settings.database_host}",
            f"--database-port={settings.database_port}",
            f"--database-name={settings.database_name}",
            f"--database-table=public.pyway",
            f"--database-migration-dir=migrations"
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        logger.error("Pyway migration failed:")
        logger.error(result.stderr)
        raise RuntimeError("Pyway failed")
    else:
        logger.info("Pyway migration applied:")
        logger.info(result.stdout)


def make_database_url(settings: Settings):
    return f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
