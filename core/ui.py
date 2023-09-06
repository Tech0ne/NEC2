import sys

from rich import print
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

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

def run_client():
    pass

def setup_server():
    if Confirm.ask("Do you want to use ngrok"):
        from pyngrok import ngrok

        authtoken = Prompt.ask("Ngrok auth token (get it [link=https://dashboard.ngrok.com/get-started/setup]here[/link])")
        ngrok.set_auth_token(authtoken)