

from cmd import Cmd
import sys

from termcolor import colored

from app.database.db_actions import add_model


class Cli(Cmd):
    file = None
    intro = colored("  Type help or ? to list commands.\n", "cyan")
    user_prompt = "$"
    prompt = colored(f"{user_prompt}-> ", "green")

    def do_add(self, line) -> None:
        add_model(line)
        # west = add_model(line)
        # print("west:",west)

    def do_prompt(self, new_prompt):
        self.user_prompt = new_prompt
        self.prompt = f"{colored(f'{self.user_prompt}-> ','green')}"


    def do_quit(self, _):
        sys.exit()

    def do_exit(self, _) -> None:
        self.do_quit(self)

    def do_end(self, _) -> None:
        self.do_quit(self)