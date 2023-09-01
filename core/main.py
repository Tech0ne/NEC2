from .encryptions import *
from .ui import *
from time import sleep

def main(args: list) -> int:
    show_help(args)
    is_server = "-server" in args
    if is_server:
        # setup_server()
        pass

    x = LiveText(title="Hello")
    sleep(1)
    x.append("Hello")
    sleep(1)
    x.append("How are u ?")
    sleep(1)
    x.stop()
