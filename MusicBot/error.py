from colorama import Fore
def error(Text: str):
    """Will take the text and set it as a error"""
    print(f"{Fore.RED}[ERROR]: {Text}")

def warn(Text: str):
    """Will take the text and set it as a error"""
    print(f"{Fore.CYAN}[WARN]: {Text}")

def log(Text: str):
    """Will log what ever is put in"""
    print(f"{Fore.GREEN}[LOG]: {Text}")