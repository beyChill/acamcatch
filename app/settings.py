from dataclasses import dataclass
from pathlib import Path
from pydantic_settings import BaseSettings
from functools import lru_cache


# @dataclass(slots=True, frozen=True, eq=False, repr=False)
class Settings(BaseSettings):
    db_name: str = "acamchat.sqlite3"
    db_config: str = "create_tables.sql"
    db_folder: str = "database/db"
    parent_dir: Path = Path(__file__).parent
    DB_PATH: Path = Path(parent_dir, db_folder, db_name)
    DB_TABLES: Path = Path(parent_dir, Path(db_folder).parent, db_config)
    DOWNLOAD_DIR: str = "/home/tom/atom/_kate"
    log_level: str = "DEBUG"


@lru_cache()
def get_settings(**kwargs: dict) -> Settings:
    return Settings(**kwargs)
