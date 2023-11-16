#!/usr/bin/env python3

import os
import sys
import shutil
import argparse
import zipencrypt
from utils.byte import bytes_to_str
from mitel.errors import NotFoundError
from mitel.firmware_pw import decode_fw_pw_bundle
from utils.string import str_to_bytes, print_new_line

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        description = "extract encrypted usb flasher upk files")

    parser.add_argument("upk_location", type=str, help="location of the .upk file")

    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

    if args.upk_location:
        if os.path.isfile(args.upk_location):
            full_upk_path = os.path.realpath(args.upk_location)
            folder_path_of_upk = os.path.dirname(full_upk_path)
            file_name = os.path.basename(full_upk_path)

            extract_dir = os.path.join(folder_path_of_upk, f"_{file_name}.extracted")
            if os.path.isdir(extract_dir):
                shutil.rmtree(extract_dir)

            with zipencrypt.ZipFile(full_upk_path, "r") as zipf:
                bundle = decode_fw_pw_bundle(bytes_to_str(zipf.comment))

                print_new_line()
                print(f"extracting {file_name} to {extract_dir}")
                print(f"zip comment: '{bundle[2]}'")
                print(f"zip password: '{bundle[1]}'")
                print(f"zip uuid string: '{bundle[0]}'")
                print_new_line()

                zipf.extractall(extract_dir, pwd=str_to_bytes(bundle[1]))
                print("done decompressing")

        else:
            raise NotFoundError("file not found") from None
