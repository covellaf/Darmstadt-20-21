#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

"""
#  Collection of OS related convenience functions.

## License
( c ) 2021 Nikolai von Krusenstiern, OPS-OAX
[MIT](https://gitlab.esa.int/xmmintfct/acc_patch/TMPrint/-/blob/develop/LICENSE)
"""


import datetime
import os
import sys
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from pathlib import Path
from typing import Dict, Generator, List, TextIO, Tuple
from zipfile import ZipFile

import script_tools.log as log
from script_tools.log import Log
from tmprint.constant import Constant


def main() -> None:
    """Main."""
    raise TypeError("'module' object is not callable")


class OsFunction(object):
    """
    Collection of OS related convenience functions.
    """

    @staticmethod
    @log.dump_args
    def dir_exists(path_as_str: str) -> bool:
        """Check if dir exists and is a dir."""
        return Path(path_as_str).is_dir()

    @staticmethod
    @log.dump_args
    def file_exists(path_as_str: str) -> bool:
        """Check if file exists and is a dir."""
        return Path(path_as_str).is_file()

    @staticmethod
    @log.dump_args
    def get_sub_dirs(folder: str) -> List[str]:
        """Collect sub-dirs in folder."""
        folder_names: List[str] = [
            f.name for f in os.scandir(Path(folder)) if f.is_dir()
        ]
        return folder_names

    @staticmethod
    @log.dump_args
    def get_files_in_dir(folder: str) -> List[str]:
        """Collect files in folder."""
        file_names: List[str]
        if OsFunction.dir_exists(folder):
            file_names = [f.name for f in os.scandir(Path(folder)) if f.is_file()]
        else:
            file_names = None
        return file_names

    @staticmethod
    @log.dump_args
    def get_files_in_dir_tree(folder: str) -> List[str]:
        """Collect tree of dirs and files in folder."""
        list_of_files: List[str] = []
        for root, _, files in os.walk(folder, topdown=True):
            for name in files:
                file_path = os.path.join(root, name)
                list_of_files.append(file_path)
        return list_of_files

    @staticmethod
    @log.dump_args
    def get_folder_lists(
        source: str,
        destination: str,
    ) -> Tuple[List[str], List[str], List[str], List[str]]:
        """
        Collect folders:
        - all folders in the destination directory
        - or the ones which are in the source directory but not in the destination.
        """
        folders_in_source: List[str] = sorted(OsFunction.get_sub_dirs(source))
        folders_in_destination: List[str] = sorted(OsFunction.get_sub_dirs(destination))

        folders_not_in_source: List[str] = sorted(
            (set(folders_in_destination) - set(folders_in_source)),
            reverse=True,
        )
        folders_not_in_destination: List[str] = sorted(
            (set(folders_in_source) - set(folders_in_destination)),
            reverse=True,
        )

        return (
            folders_in_source,
            folders_not_in_source,
            folders_in_destination,
            folders_not_in_destination,
        )

    @staticmethod
    @log.dump_args
    def is_png(file_: str) -> bool:
        """Check if file name extension is .png."""
        is_png: bool = os.path.splitext(file_)[1].lower() == ".png"
        return is_png

    @staticmethod
    @log.dump_args
    def dir_exists_or_exit(path: str) -> bool:
        """Check if directory exists, exit if not"""
        if not OsFunction.dir_exists(path):
            Log.logger.warning(f"'{path}' is not a valid directory path")
            sys.exit(1)
        return True

    @staticmethod
    @log.dump_args
    def sub_dirs_exist_or_exit(path: str, folders: List[str]) -> bool:
        """Check if list of sub-directory exists, exit if not."""
        for folder in folders:
            dir_path = os.path.join(path, folder)
            OsFunction.dir_exists_or_exit(dir_path)
        return True

    @staticmethod
    @log.dump_args
    def create_dict_for_zipping_files_with_their_relative_path(
        path_to_base_of_realtive_path: str,
        relative_file_path_within_zip: str,
        files_with_realtive_path: List[str],
    ) -> Dict[str, str]:
        """Create dict with relative path for zip file creation."""
        file_dict: Dict[str, str] = {}

        path_to_files: str = os.path.join(
            path_to_base_of_realtive_path,
            relative_file_path_within_zip,
        )

        if files_with_realtive_path:
            for file_name in files_with_realtive_path:
                file_path: str = os.path.join(path_to_files, file_name)
                file_rel: str = os.path.relpath(
                    file_path,
                    path_to_base_of_realtive_path,
                )
                file_dict[file_path] = file_rel

        return file_dict

    @staticmethod
    @log.dump_args
    def zip_files_with_relative_path_from_dict(
        zip_file_path: str,
        file_dict: Dict[str, str],
    ) -> bool:
        """zip files in file_dict: path, relative path."""

        with ZipFile(
            zip_file_path,
            "w",
            compression=Constant.COMPRESSION,
        ) as zip_file:

            for file_path, file_rel in file_dict.items():
                Log.debug(
                    f"Loop item: zip_file.write({file_path=}, {file_rel=})",
                    level=Log.LOG_DICT["LOOP"],
                )
                zip_file.write(file_path, file_rel)

    @staticmethod
    @log.dump_args
    def get_last_update_time_of_file(file_path: str) -> str:
        """Get last update time for a given file path."""

        time_file_updated = datetime.datetime.fromtimestamp(
            file_path.stat().st_ctime,
        ).strftime(Constant.DATETIME_FORMAT)

        return time_file_updated

    @staticmethod
    @log.dump_args
    def get_time_stamp_in_utc() -> str:
        """Get current date time string in utc."""
        now_date_time_utc = datetime.datetime.utcnow().strftime(
            Constant.DATETIME_FORMAT,
        )
        return now_date_time_utc

    @staticmethod
    @contextmanager
    def redirect_all_out(
        file_handle: TextIO,
    ) -> Generator[Tuple[TextIO, TextIO], None, None]:
        """Redirect all output, from stdout and from stderr."""
        with redirect_stdout(file_handle) as out, redirect_stderr(file_handle) as err:
            yield (out, err)


if __name__ == "__main__":
    main()
