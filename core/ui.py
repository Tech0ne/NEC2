import sys

from rich import print
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.live import Live
from rich.table import Table

from threading import Thread, Event


def show_help(args: list):
    if "--help" in args or "-h" in args:
        string =    f"""Chat with [italic]everyone[not italic], everywhere !

Usage:
+ [bold blue]Client[not bold white]
    [cyan]{args[0]}[white] [khaki3]\[options][white] [purple]\[IP][white] [dark_orange3]\[PORT][white]
    Connect to [purple]\[IP][white] on port [dark_orange3]\[PORT][white] for chatting.
    [khaki3]Options[white]:
        --help, -h      Show this help and exit

+ [bold blue]Server[not bold white]
    [cyan]{args[0]}[white] -server [khaki3]\[options][white] [dark_orange3]\[PORT][white]
    Opens port [dark_orange3]\[PORT][white] as a server. By default, it will also connect to it for chatting.
    [khaki3]Options[white]:
        --help, -h      Show this help and exit
        print(Panel("Usage :"))"""
        print(Panel(string, title="[red]CommunityChat[white]", title_align="center"))
        sys.exit(2)