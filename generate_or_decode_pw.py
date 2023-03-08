#!/usr/bin/env python3

import sys
import argparse
from mitel.firmware_pw import generate_fw_pw_bundle, decode_fw_pw_bundle

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        description = "generate or decode password for Aastra/DeTeWe/Mitel .upk zipped firmwares")

    subparsers = parser.add_subparsers(help="sub-command help", dest="subparser_name")

    generate_parser = subparsers.add_parser("generate", help="generate a firmware package comment and password combo.")

    decode_parser = subparsers.add_parser("decode", help="decode a firmware package comment to reveal the password.")
    decode_parser.add_argument("zip_comment", type=str, help="zip comment of the firmware package, use single quotes to wrap the text.")

    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

    bundle = None
    if args.subparser_name == "generate":
        bundle = generate_fw_pw_bundle()
    elif args.subparser_name == "decode":
        bundle = decode_fw_pw_bundle(args.zip_comment)

    if bundle is not None:
        print(f"firmware uuid string: '{bundle[0]}'")
        print(f"firmware zip password: '{bundle[1]}'")
        print(f"firmware zip comment: '{bundle[2]}'")
