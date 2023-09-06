from .encryptions import *
from .ui import *

def main(args: list) -> int:
    if "--help" in args or "-h" in args:
        show_help(args)
    is_server = "-server" in args
    if is_server:
        pass

    run_client()
    setup_server()