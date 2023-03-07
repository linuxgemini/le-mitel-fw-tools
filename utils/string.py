def str_to_hexstr(s: str) -> str:
    return bytes(s, "utf-8").hex().lower()


def str_to_bytes(s: str) -> bytes:
    return bytes(s, "utf-8")


def hexstr_to_bytes(hexstr: str) -> bytes:
    return bytes.fromhex(hexstr)

def print_new_line(amount: int = 1) -> None:
    if amount < 1: raise ValueError("amount can't be less than 1")
    for _ in range(1, amount+1):
        print("")
