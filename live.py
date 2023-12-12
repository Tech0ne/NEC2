from rich import print

from rich.panel import Panel
from rich.live import Live

from threading import Thread, Event

from time import sleep

def fill_in(p, e):
    for _ in range(20):
        p.renderable += "This is another phrase "
        sleep(1)
    e.set()

p = Panel("")

with Live(p, refresh_per_second=20):
    e = Event()
    Thread(target=fill_in, args=(p, e), daemon=True).start()
    while not e.is_set():
        sleep(0.5)
