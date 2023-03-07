def bytes_to_hexstr(b: bytes) -> str:
    return b.hex().lower()


def bytes_to_str(b: bytes) -> str:
    return b.decode()


# adapted from https://stackoverflow.com/a/3391106
def repeat_to_length(b: bytes, wanted_len: int) -> bytes:
    return (b * (wanted_len//len(b) + 1))[:wanted_len]


def xor(var: bytes, key: bytes) -> bytes:
    if len(key) > len(var):
        key_to_use = key[0:len(var)]
    elif len(key) < len(var):
        key_to_use = repeat_to_length(key, len(var))
    else:
        key_to_use = key

    return bytes(a ^ b for a, b in zip(var, key_to_use, strict=True))
