from contextlib import contextmanager
from logging import getLogger
from pathlib import Path
import sqlite3
import time
from typing import Any, Generator
from datetime import date
from termcolor import colored
from calendar import timegm
from app.settings import get_settings


log = getLogger(__name__)

DB_PATH = get_settings().DB_PATH
DB_TABLES = get_settings().DB_TABLES


@contextmanager
def connect() -> Generator[sqlite3.Cursor, Any, None]:
    with sqlite3.connect(DB_PATH) as connect:
        yield connect.cursor()


def db_init() -> None:
    if DB_PATH.exists():
        log.info(colored("Database is active", "cyan"))
        return None

    try:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        log.info(colored("Initializing new database", "cyan"))

        with connect() as cursor:
            with open(DB_TABLES, "r", encoding="utf-8") as file:
                cursor.executescript(file.read())

            log.info(colored("Database is active", "cyan"))

    except sqlite3.OperationalError as error:
        log.error(error)
    return None


# ***********************************
# * WRITE
# ***********************************


def add_model(name_: str) -> bool:
    today = date.today()
    sql = f"INSERT INTO chaturbate (streamer_name, query_time, follow) VALUES ( ?, ?, ?) ON CONFLICT (streamer_name) DO UPDATE SET follow='{today}'"
    args = (name_, timegm(time.gmtime()), date.today())
    write = _write_to_db(sql, args)
    if not write:
        log.error("Failed to add: %s", (colored(name_, "red")))
    return bool(write)


def _write_to_db(sql, arg) -> bool:
    try:
        with connect() as cursor:
            write = cursor.execute(sql, arg)
    except sqlite3.Error as error:
        log.error(error)
        write = None
    return bool(write)
