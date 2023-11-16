#!/usr/bin/env python3

import os
import sys
import shutil
import tarfile
import argparse
import tempfile
import zipencrypt
from mitel.errors import NotFoundError
from mitel.firmware_pw import generate_fw_pw_bundle
from utils.string import str_to_bytes, print_new_line

def recursively_add_to_zip(path: str, zip_handle: zipencrypt.ZipFile, password: bytes = None) -> None: # type: ignore
    for root, dirs, files in os.walk(path):
        for file in files:
            print(f"adding \"{file}\"")
            zip_handle.write(os.path.join(root, file),
                             os.path.relpath(os.path.join(root, file),
                                             os.path.join(path, "..")),
                             pwd=password)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        description = "convert unencrypted dnld bundles to usb flasher upk files")

    parser.add_argument("dnld_location", type=str, help="location of the unencrypted .dnld file")

    args = parser.parse_args(args=None if sys.argv[1:] else ["--help"])

    if args.dnld_location:
        if os.path.isfile(args.dnld_location):
            full_dnld_path = os.path.realpath(args.dnld_location)
            folder_path_of_dnld = os.path.dirname(full_dnld_path)
            file_name = os.path.basename(full_dnld_path)

            with tempfile.TemporaryDirectory() as tempdir_path:
                extract_dir = os.path.join(tempdir_path, "extract")
                firmwares = []

                full_temp_dnld_path = os.path.join(tempdir_path, file_name)
                shutil.copyfile(full_dnld_path, full_temp_dnld_path)

                with tarfile.open(full_temp_dnld_path, "r:gz") as dnld_archive:
                    dnld_archive.extractall(extract_dir)

                with open(os.path.join(extract_dir, "mddf.ini"), mode="r", encoding="utf-8") as mddf:
                    buffer = {}
                    for line in mddf:
                        if line.startswith("PATH") and len(buffer) == 0:
                            buffer["fw_image_folder"] = os.path.dirname(os.path.join(extract_dir, line.split(" = ")[1][:-1]))
                        elif line.startswith("HSTYPE") and buffer.get("fw_image_folder"):
                            buffer["fw_handset_type"] = line.split(" = ")[1][:-1]
                        elif line.startswith("VERSION") and buffer.get("fw_image_folder"):
                            buffer["fw_version"] = line.split(" = ")[1][:-1]
                        elif line.startswith("MD5") and buffer.get("fw_image_folder"):
                            buffer["fw_md5sum"] = line.split(" = ")[1][:-1]

                        if buffer.get("fw_image_folder") and \
                           buffer.get("fw_handset_type") and \
                           buffer.get("fw_version") and \
                           buffer.get("fw_md5sum"):
                            firmwares.append(buffer)
                            buffer = {}

                for firmware in firmwares:
                    fw_image_folder = firmware["fw_image_folder"]
                    fw_image_name = os.path.basename(fw_image_folder)

                    fw_filename = f"{fw_image_name.split('_')[0].upper()}-{firmware['fw_version']}.upk"

                    with tempfile.TemporaryDirectory() as fw_tmpdir_path:
                        fw_packaging_dir = os.path.join(fw_tmpdir_path, "firmware")
                        shutil.copytree(fw_image_folder, fw_packaging_dir)

                        if os.path.isfile(fw_filename):
                            os.remove(fw_filename)

                        with zipencrypt.ZipFile(os.path.join(folder_path_of_dnld, fw_filename), "w", zipencrypt.ZIP_DEFLATED) as zipf:
                            bundle = generate_fw_pw_bundle()

                            print_new_line()
                            print(f"creating {fw_filename}")
                            print(f"zip uuid string: '{bundle[0]}'")
                            print(f"zip password: '{bundle[1]}'")
                            print(f"zip comment: '{bundle[2]}'")
                            print_new_line()

                            zipf.comment = str_to_bytes(bundle[2])
                            recursively_add_to_zip(fw_packaging_dir, zipf, str_to_bytes(bundle[1]))
                            print("done compressing")

        else:
            raise NotFoundError("file not found") from None
