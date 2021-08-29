#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

"""
#  Collection of OS related convenience functions.

## License
( c ) 2021 Nikolai von Krusenstiern, OPS-OAX
[MIT](https://gitlab.esa.int/xmmintfct/acc_patch/TMPrint/-/blob/develop/LICENSE)
"""


import sys
from typing import List

import script_tools.log as log
from script_tools.log import Log
from script_tools.os_function import OsFunction
from tmprint.config import ApiConf, config
from tmprint.constant import Constant


def main() -> None:
    """Main."""
    raise TypeError("'module' object is not callable")


class AnalyzeFolders(object):
    """
    Collection of OS related convenience functions.
    """

    @staticmethod
    @log.dump_args
    def get_folders_to_update(  # noqa: C901
        source: str,
        destination: str,
    ) -> List[str]:
        """
        Based on command line options and arguments, return folders to update
        """
        folders_in_source: List[str]
        folders_not_in_source: List[str]

        folders_in_destination: List[str]
        folders_not_in_destination: List[str]

        folders_to_update: List[str]

        Log.logger.info(f"Browse Plots at: {Constant.REMOTE_URL}")

        if ApiConf.folder_to_update_api:
            folders_to_update = [ApiConf.folder_to_update_api]
            return folders_to_update

        (
            folders_in_source,
            folders_not_in_source,
            folders_in_destination,
            folders_not_in_destination,
        ) = OsFunction.get_folder_lists(source, destination)

        if config.plot_data_all:
            config.plot_data = folders_in_source

        if config.plot_data:
            folders_to_update = config.plot_data
            Log.logger.info(f"{folders_to_update=}")  # noqa: E1120, E1123
            return folders_to_update

        if config.update_html_all:
            config.update_html = folders_in_destination

        if config.update_html:
            folders_to_update = config.update_html
            Log.logger.info(f"{folders_to_update=}")
            return folders_to_update

        if config.list_data_dirs:
            folder_list = " ".join(folders_in_source)
            print(f"Folders in {source}: {folder_list}")
            sys.exit(0)

        if config.list_plot_dirs:
            folder_list = " ".join(folders_in_destination)
            print(f"Folders in {destination}: {folder_list}")
            sys.exit(0)

        if config.list_missing_plot_dirs:
            folder_list = " ".join(folders_not_in_destination)
            print(f"Folders missing in {destination}: {folder_list}")
            sys.exit(0)

        if config.list_missing_data_dirs:
            folder_list = " ".join(folders_not_in_source)
            print(f"Folders missing in {source}: {folder_list}")
            sys.exit(0)

        Log.logger.info(f"{folders_not_in_destination=}")
        return folders_not_in_destination


if __name__ == "__main__":
    main()
