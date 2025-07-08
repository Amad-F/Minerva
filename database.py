from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import urlparse, urlunparse
from config import Config


Base = declarative_base()
_engine = None

def ensure_database_exists(db_url_str):
    parsed_url = urlparse(db_url_str)
    db_name = parsed_url.path.lstrip('/')
    if not db_name:
        raise ValueError("Database name is empty in DATABASE_URL")

    server_url = urlunparse(parsed_url._replace(path=""))
    temp_engine = create_engine(server_url)
    try:
        with temp_engine.connect() as connection:
            connection.execute(text(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            connection.commit()
            print(f"Database '{db_name}' ensured to exist.")
    finally:
        temp_engine.dispose()

def get_engine():
    global _engine
    if _engine is None:
        db_url = Config.DATABASE_URL
        ensure_database_exists(db_url)
        _engine = create_engine(db_url)
    return _engine

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

def create_db_tables():
    
    from models import AgentInteraction, GeneratedQuiz
    engine = get_engine()
    try:
        print("Creating Minerva database tables...")
        Base.metadata.create_all(engine)
        print("Tables checked/created successfully.")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        raise
