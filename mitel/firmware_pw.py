import re
from uuid import uuid4
from mitel.errors import *
from utils.byte import *
from utils.string import *


### start of constants ###
zip_comment_regex = re.compile(r"^\$\$([0-9a-fA-F]{76})\$\$$")
mitel_xor_key = hexstr_to_bytes("7f044e1c91727f207f044e1c91727f20")
### end of constants ###


def generate_uuid() -> str:
    return f"{{{str(uuid4())}}}".lower()


def generate_zip_password_from_uuid(fw_uuid: str) -> str:
    return str_to_hexstr(fw_uuid)


def generate_zip_comment_from_uuid(fw_uuid: str) -> str:
    fw_uuid_bytes = str_to_bytes(fw_uuid)
    zip_comment_bytes = xor(fw_uuid_bytes, mitel_xor_key)
    zip_comment_hexstr = bytes_to_hexstr(zip_comment_bytes)

    return f"$${zip_comment_hexstr}$$"


def get_fw_uuid_rawbytes(zip_hexstr: str) -> bytes:
    zip_hexstr_bytes = hexstr_to_bytes(zip_hexstr)
    fw_uuid_bytes = xor(zip_hexstr_bytes, mitel_xor_key)

    return fw_uuid_bytes


def get_fw_uuid_from_zip_comment(zip_hexstr: str) -> str:
    return bytes_to_str(get_fw_uuid_rawbytes(zip_hexstr))


def generate_fw_pw_bundle() -> tuple[str, str, str]:
    fw_uuid = generate_uuid()
    zip_pw = generate_zip_password_from_uuid(fw_uuid)
    zip_comment = generate_zip_comment_from_uuid(fw_uuid)

    return (fw_uuid, zip_pw, zip_comment)


def decode_fw_pw_bundle(zip_comment: str) -> tuple[str, str, str]:
    matched_comment = zip_comment_regex.match(zip_comment)
    if not matched_comment:
        raise ValueError("given zip_comment is not valid")
    fw_uuid = get_fw_uuid_from_zip_comment(matched_comment[1])
    zip_pw = generate_zip_password_from_uuid(fw_uuid)

    return (fw_uuid, zip_pw, zip_comment)


def decode_fw_pw(zip_comment: str) -> str:
    matched_comment = zip_comment_regex.match(zip_comment)
    if not matched_comment:
        raise ValueError("given zip_comment is not valid")
    zip_pw = get_fw_uuid_rawbytes(matched_comment[1])

    return bytes_to_hexstr(zip_pw)
