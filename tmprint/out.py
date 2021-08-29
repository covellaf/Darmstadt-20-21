#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

"""
#  Create files in new directory.

## License
( c ) 2021 Nikolai von Krusenstiern, OPS-OAX
[MIT](https://gitlab.esa.int/xmmintfct/acc_patch/TMPrint/-/blob/develop/LICENSE)
"""


import os
import shutil
from contextlib import nullcontext, redirect_stdout
from typing import ContextManager, Dict, List, Optional, TextIO, Tuple, Union

import TMPrint_client

import script_tools.log as log
from script_tools.log import Log
from script_tools.os_function import OsFunction
from tmprint.config import config
from tmprint.constant import Constant
from tmprint.html import HTML


def main() -> None:
    """Main."""
    raise TypeError("'module' object is not callable")


class Out(object):
    """
    Create files in new directory.

    - plots via external script (png)
        - creates new directory
    - copies remark.html from data to plot directory
    - build index.html file
    - zip file of new directory
    """

    @staticmethod
    @log.dump_args
    def copy_remark_file(
        data_folder_path: str,
        plot_folder_path: str,
        folder_to_update: str,
    ) -> None:
        """Copy remark.html file form data to plot directory, if any"""
        source_path: str = os.path.join(data_folder_path, folder_to_update)
        destination_path: str = os.path.join(plot_folder_path, folder_to_update)

        remark_file_source: str = os.path.join(
            source_path,
            Constant.REMARK_FILE_NAME,
        )
        remark_file_destination: str = os.path.join(
            destination_path,
            Constant.REMARK_FILE_NAME,
        )

        Log.debug(f"{remark_file_source=}", level=Log.LOG_DICT["VAR"])
        Log.debug(f"{remark_file_destination=}", level=Log.LOG_DICT["VAR"])

        if OsFunction.file_exists(remark_file_source):
            Log.logger.info(f"Copy {Constant.REMARK_FILE_NAME} to {destination_path}")
            shutil.copyfile(remark_file_source, remark_file_destination)
        else:
            Log.logger.info(f"No {Constant.REMARK_FILE_NAME} in {source_path}")

    @staticmethod
    @log.dump_args
    def call_plot_tool(
        data_folder_path: str,
        plot_folder_path: str,
        folder_to_update: str,
    ) -> None:
        """Call external plot tool."""

        if config.update_html:
            Log.logger.info(f"Working on {folder_to_update=}")
            return

        Log.logger.info(f"Generate plots for {folder_to_update=}")
        Log.debug(
            f"Calling: plot_tool({data_folder_path=} \
            {plot_folder_path=} {folder_to_update=}",
            level=Log.LOG_DICT["EXTERNAL"],
        )

        # NvK: remove context managers, when plot_tool is quiet
        dev_null: TextIO = open(os.devnull, "w")

        contex_manager: ContextManager[Optional[Union[TextIO, Tuple[TextIO, TextIO]]]]

        if (
            Log.console_level <= Log.LOG_DICT["STDOUT"]
            or Constant.CALL_SCRIPT_NO_FILTER  # noqa: W503
        ):
            contex_manager = nullcontext()
        elif (
            Log.console_level >= Log.LOG_DICT["CRITICAL"]
            or Constant.CALL_SCRIPT_FROM_CRON  # noqa: W503
        ):
            contex_manager = OsFunction.redirect_all_out(dev_null)
        else:
            contex_manager = redirect_stdout(dev_null)

        with contex_manager:
            TMPrint_client.plot_tool(
                folder_to_update,
                data_folder_path,
                plot_folder_path,
            )

    @staticmethod
    @log.dump_args
    def create_html_and_zip_file_for_plot_dir(
        plot_folder_path: str,
        folder_to_update: str,
    ) -> None:
        """Call index.html and zip file creation."""
        args_for_html: List[str]
        args_for_zip: List[str]

        args_for_html, args_for_zip = Out.create_arg_tuples_for(
            plot_folder_path,
            folder_to_update,
        )
        HTML.create_file(*args_for_html)
        Out.create_zip_file_for_plot_dir(*args_for_zip)

    @staticmethod
    @log.dump_args
    def create_arg_tuples_for(
        plot_folder_path: str,
        folder_to_update: str,
    ) -> Tuple[Tuple[str, str, List[str], List[str]], Tuple[str, str, List[str]]]:
        """Collect files in plot folder, create sets of files for index.html and zip."""

        folder_to_update_path: str = os.path.join(plot_folder_path, folder_to_update)
        zip_file_name: str = f"{folder_to_update}.zip"

        file_names: List[str] = list(
            set(OsFunction.get_files_in_dir(folder_to_update_path))
            - {  # noqa: C812, W503
                Constant.INDEX_FILE_NAME,
                Constant.REMARK_FILE_NAME,
                zip_file_name,
            },
        )

        file_names_including_html_file: List[str] = file_names + [
            Constant.INDEX_FILE_NAME,
        ]

        png_files: List[str] = [x for x in file_names if OsFunction.is_png(x)]
        other_files_with_zip: List[str] = list(set(file_names) - set(png_files)) + [
            zip_file_name  # noqa: C812
        ]

        args_for_html = (
            plot_folder_path,
            folder_to_update,
            other_files_with_zip,
            png_files,
        )

        args_for_zip = (
            plot_folder_path,
            folder_to_update,
            file_names_including_html_file,
        )

        Log.debug(f"{args_for_html=}", level=Log.LOG_DICT["VAR"])
        Log.debug(f"{args_for_zip=}", level=Log.LOG_DICT["VAR"])

        return args_for_html, args_for_zip

    @staticmethod
    @log.dump_args
    def create_zip_file_worker(
        folder_root: str,
        relative_folder: str,
        list_of_file_names_in_folder: List[str],
        zip_file_path: str,
    ) -> None:
        """
        Create a zip file based on a list of files from given directory.
        Save the files in the zip file with a relative path
        from another given directory.
        """

        Log.debug(f"Create zip file for Plots of {relative_folder=}")
        Log.debug(f"{zip_file_path=}", level=Log.LOG_DICT["VAR"])

        file_dict: Dict[
            str,
            str,
        ] = OsFunction.create_dict_for_zipping_files_with_their_relative_path(
            folder_root,
            relative_folder,
            list_of_file_names_in_folder,
        )

        if file_dict:
            OsFunction.zip_files_with_relative_path_from_dict(zip_file_path, file_dict)

    @staticmethod
    @log.dump_args
    def create_zip_file_for_plot_dir(
        plot_folder_path: str,
        folder_to_update: str,
        file_names_including_html_file: List[str],
    ) -> None:
        """
        Create a zip file based on a list of files from given directory.
        Save the files in the zip file with a relative path
        from another given directory.
        """

        zip_file_name: str = f"{folder_to_update}.zip"
        zip_file_path_root: str = os.path.join(plot_folder_path, folder_to_update)
        zip_file_path: str = os.path.join(zip_file_path_root, zip_file_name)

        Out.create_zip_file_worker(
            plot_folder_path,
            folder_to_update,
            file_names_including_html_file,
            zip_file_path,
        )

    @staticmethod
    @log.dump_args
    def create_zip_file_for_data_dir(
        data_folder_path: str,
        plot_folder_path: str,
        folder_to_update: str,
    ) -> None:
        """Create a zip file for the data folder."""
        zip_file_name: str = f"data_{folder_to_update}.zip"
        zip_file_path_root: str = os.path.join(plot_folder_path, folder_to_update)
        zip_file_path: str = os.path.join(zip_file_path_root, zip_file_name)

        data_folder: str = os.path.join(data_folder_path, folder_to_update)
        data_files: List[str] = OsFunction.get_files_in_dir(data_folder)

        Out.create_zip_file_worker(
            data_folder_path,
            folder_to_update,
            data_files,
            zip_file_path,
        )


if __name__ == "__main__":
    main()
