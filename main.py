from app.database.db_actions import db_init
from app.log.logger import setup_logging
from app.ui.command_line import Cli


if __name__ == "__main__":
    setup_logging()
    db_init()
    Cli().cmdloop()