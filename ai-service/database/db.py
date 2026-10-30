import logging
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from config.settings import settings

logger = logging.getLogger("travelsync.db")

# -----------------------------------------------------------------------
# Engine — prefers PostgreSQL, silently falls back to SQLite for local dev
# -----------------------------------------------------------------------

DATABASE_URL = settings.DATABASE_URL

try:
    if DATABASE_URL.startswith("postgresql"):
        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
        )
    else:
        # SQLite — local development default
        engine = create_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False},
        )
    logger.info(f"Database engine created: {DATABASE_URL.split('://')[0]}")
except Exception as e:
    logger.warning(f"Primary DB unavailable ({e}), falling back to SQLite.")
    DATABASE_URL = "sqlite:///./travelsync.db"
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# -----------------------------------------------------------------------
# FastAPI dependency — yields a DB session and closes it on completion
# -----------------------------------------------------------------------

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------------------------------------------------
# Create all tables from ORM models & handle lightweight migrations
# -----------------------------------------------------------------------

def init_db():
    """Creates all database tables if they don't already exist and applies schema sync."""
    from database import models  # noqa: F401 — ensures models are registered
    Base.metadata.create_all(bind=engine)

    # Lightweight migration for existing databases
    with engine.connect() as conn:
        try:
            # Check trips columns
            if not str(engine.url).startswith("postgresql"):
                result = conn.execute(text("PRAGMA table_info(trips);")).fetchall()
                columns = [row[1] for row in result]
                trip_cols_to_add = [
                    ("user_id", "VARCHAR"),
                    ("title", "VARCHAR"),
                    ("status", "VARCHAR DEFAULT 'upcoming'"),
                    ("is_saved", "BOOLEAN DEFAULT 1"),
                    ("share_token", "VARCHAR"),
                    ("is_public", "BOOLEAN DEFAULT 0"),
                    ("start_date", "VARCHAR"),
                    ("end_date", "VARCHAR"),
                    ("notes", "TEXT"),
                    ("tags", "TEXT DEFAULT '[]'"),
                    ("transport_mode", "VARCHAR DEFAULT 'flight'"),
                    ("transport_data", "TEXT"),
                    ("updated_at", "DATETIME")
                ]
                for col_name, col_type in trip_cols_to_add:
                    if columns and col_name not in columns:
                        conn.execute(text(f"ALTER TABLE trips ADD COLUMN {col_name} {col_type};"))
                        conn.commit()

                # Check activities columns
                act_res = conn.execute(text("PRAGMA table_info(activities);")).fetchall()
                act_cols = [row[1] for row in act_res]
                if act_cols and "created_at" not in act_cols:
                    conn.execute(text("ALTER TABLE activities ADD COLUMN created_at DATETIME;"))
                    conn.commit()

                # Check flights columns
                fl_res = conn.execute(text("PRAGMA table_info(flights);")).fetchall()
                fl_cols = [row[1] for row in fl_res]
                if fl_cols and "created_at" not in fl_cols:
                    conn.execute(text("ALTER TABLE flights ADD COLUMN created_at DATETIME;"))
                    conn.commit()

                # Check users columns
                user_res = conn.execute(text("PRAGMA table_info(users);")).fetchall()
                user_cols = [row[1] for row in user_res]
                user_cols_to_add = [
                    ("profile_picture", "VARCHAR"),
                    ("phone", "VARCHAR"),
                    ("two_factor_enabled", "BOOLEAN DEFAULT 0"),
                    ("travel_preferences", "TEXT DEFAULT '{}'"),
                    ("notification_preferences", "TEXT DEFAULT '{}'"),
                    ("appearance_preferences", "TEXT DEFAULT '{}'"),
                    ("privacy_preferences", "TEXT DEFAULT '{}'"),
                    ("travel_documents", "TEXT DEFAULT '{}'"),
                    ("updated_at", "DATETIME")
                ]
                for col_name, col_type in user_cols_to_add:
                    if user_cols and col_name not in user_cols:
                        conn.execute(text(f"ALTER TABLE users ADD COLUMN {col_name} {col_type};"))
                        conn.commit()
                logger.info("Schema migration complete for SQLite.")
        except Exception as e:
            logger.debug(f"Schema check pragma note: {e}")

    logger.info("Database tables initialized successfully.")
