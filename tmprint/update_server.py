#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
# update local files to int2darc
"""

import os
import shutil
import sys
from pathlib import Path

from script_tools.log import Log
from script_tools.os_function import OsFunction


class Main(object):
    """
    Main class
    """

    @staticmethod
    def main() -> None:
        """Main loop."""
        if len(sys.argv) > 1:
            Update.scp_source_to_destinantion()
            sys.exit(1)

        Log.setup()
        Update.check_files_or_exit()
        Update.copy_source_to_temp()
        Update.copy_destination_to_temp()
        Update.zip_destination_in_temp()


class Update(object):
    """
    # update local files to int2darc
    """

    source_path = "/Users/nkrusens/esabox/Developer/python/tmprint"

    temp_path = "/tmp/TMPrint"
    source_temp_path = "/tmp/TMPrint/source"
    destination_temp_path = "/tmp/TMPrint/destination"

    destination = "imcsuser@int2darc.esoc.esa.int"
    destination_path = "/home/imcsuser/TMPrint/Application_Launcher"

    source_files = [
        "script_tools/log.py",
        "script_tools/os_function.py",
        "script_tools/scp.py",
        "script_tools/tools.py",
        "tmprint/analyze_folders.py",
        "tmprint/config.py",
        "tmprint/constant.py",
        "tmprint/html.py",
        "tmprint/out.py",
        "tmprint/parser.py",
        "tmprint/watch_folder.py",
    ]

    destination_files = [
        "script_tools/log.py",
        "script_tools/os_function.py",
        "script_tools/scp.py",
        "script_tools/tools.py",
        "tmprint/analyze_folders.py",
        "tmprint/config.py",
        "tmprint/constant.py",
        "tmprint/html.py",
        "tmprint/out.py",
        "tmprint/parser.py",
        "watch_folder.py",
    ]

    @staticmethod
    def check_files_or_exit() -> None:
        """check if files do exist."""
        for file_ in Update.source_files:
            file_path = os.path.join(Update.source_path, file_)
            status = OsFunction.file_exists(file_path)
            if not status:
                print(f"Error: {file_path} does not exist.")
                sys.exit(1)

    @staticmethod
    def copy_source_to_temp() -> None:
        """copy source files to temp staging area."""

        shutil.rmtree(Update.source_temp_path)

        for file_ in Update.source_files:

            sub_dir, _ = os.path.split(file_)
            source_dir = os.path.join(Update.source_temp_path, sub_dir)
            Path(source_dir).mkdir(parents=True, exist_ok=True)

            source = os.path.join(Update.source_path, file_)
            destination = os.path.join(Update.source_temp_path, file_)

            with open(source, "rt") as fin:
                with open(destination, "wt") as fout:
                    for line in fin:
                        fout.write(line.replace("python3", "python3.9"))

        main_from = os.path.join(Update.source_temp_path, "tmprint/watch_folder.py")
        shutil.move(main_from, Update.source_temp_path)

    @staticmethod
    def copy_destination_to_temp() -> None:
        """scp files from destination to temporary staging area."""

        shutil.rmtree(Update.destination_temp_path, ignore_errors=True)

        for file_ in Update.destination_files:
            sub_dir, file_name = os.path.split(file_)
            source_dir = os.path.join(Update.destination_temp_path, sub_dir)
            Path(source_dir).mkdir(parents=True, exist_ok=True)

            remote = f"{Update.destination}:{Update.destination_path}/{file_}"
            local = f"{Update.destination_temp_path}/{sub_dir}/{file_name}"
            cmd = f"scp {remote} {local}"
            os.system(cmd)

        print()
        print(f"cd {Update.temp_path}")
        print("diff-y -r source destination | more")

    @staticmethod
    def zip_destination_in_temp() -> None:
        """zip files in destination temporary staging area."""

        folder_to_zip = Update.destination_temp_path

        time_stamp = OsFunction.get_time_stamp_in_utc()
        zip_file_name = f"int2darc_{time_stamp}.zip"

        zip_file_path_root, sub_folder = os.path.split(folder_to_zip)
        zip_file_path = os.path.join(zip_file_path_root, zip_file_name)

        files = OsFunction.get_files_in_dir_tree(folder_to_zip)

        file_dict = OsFunction.create_dict_for_zipping_files_with_their_relative_path(
            zip_file_path_root,
            sub_folder,
            files,
        )

        OsFunction.zip_files_with_relative_path_from_dict(zip_file_path, file_dict)

    @staticmethod
    def scp_source_to_destinantion() -> None:
        """scp files from temporary staging area to server."""
        source = Update.source_temp_path
        destination = f"{Update.destination}:{Update.destination_path}"
        cmd = f"scp -r {source}/* {destination}"
        print()
        print(cmd)
        print()


if __name__ == "__main__":
    Main.main()
