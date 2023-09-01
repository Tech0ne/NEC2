import os

def clear_for_rich(string: str) -> str:
    return string.replace('[', "\\[").replace(':', ":\u200b")

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")