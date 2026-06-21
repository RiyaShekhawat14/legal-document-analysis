from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def ensure_schema():
    inspector = inspect(engine)

    if "documents" in inspector.get_table_names():
        document_columns = {column["name"] for column in inspector.get_columns("documents")}
        statements = []

        if "overall_risk" not in document_columns:
            statements.append("ALTER TABLE documents ADD COLUMN overall_risk VARCHAR")
        if "owner_id" not in document_columns:
            statements.append("ALTER TABLE documents ADD COLUMN owner_id INTEGER")

        if statements:
            with engine.begin() as connection:
                for statement in statements:
                    connection.execute(text(statement))


# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
