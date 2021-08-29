#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

"""
# SIM Test to Web-Server

Semi-Automatic use TM as SIM data, create plot directories and sync to web server.
See [User Manual](http://xmm.esoc.esa.int/docs/simulations/int/User_Manual.html)

## This script
- setup logging
- parse cmd line
- if folder exist in DATA and NOT in PLOT:
  - call TMPrint_client:plot_tool
  - generate index.html and zip file
  - add zip file for data dir
  - sync directory tree to web server via scp

## External inputs
- MCS TMprint, Sim.log, [remarks.html]
- plot data (created via TMPrint_client:plot_tool)

## Side Effects
- logs to watch_folder.py.log
- calls TMPrint_client:plot_tool, which creates folder with png plots
- creates an index.html file with the content of this new folder, and remarks.html
- creates a zip file of this new folder with plots and index.html file
- creates a zip file of the corresponding data folder
- copies the plot folder to the web server

## Meta
- Level: Production

### Refactor / Ideas
- use pydantic @ config.py
- suppress memory log flush at exit
- tee stdout and stderr from plot_tool -> log

### ToDo
- git
    - version numbering via git tag
- external dependencies made workarounds necessary
    - like context managers
    - wait for plot_tool to be quiet
- pytest
    - write test cases
- get external code review
    - Comments are more than welcome

## Installation
- ESA GitLab
    [Repository](https://gitlab.esa.int/xmmintfct/acc_patch/TMPrint/-/tree/develop/)

## License
( c ) 2021 Nikolai von Krusenstiern, OPS-OAX
[MIT](https://gitlab.esa.int/xmmintfct/acc_patch/TMPrint/-/blob/develop/LICENSE)
"""


import argparse
from typing import List, Optional

import script_tools.log as log
from script_tools.log import Log
from script_tools.scp import SCP
from tmprint.analyze_folders import AnalyzeFolders
from tmprint.config import ApiConf
from tmprint.constant import Constant
from tmprint.out import Out
from tmprint.parser import Parser


class Main(object):
    """
    # SIM Test to Web-Server
    """

    @staticmethod
    @log.dump_args
    def main() -> None:
        """Main."""

        Log.setup(Constant.SCRIPT_NAME)
        Constant.setup()

        args: argparse.Namespace = Parser.parse()
        data_folder_path: str = args.data
        plot_folder_path: str = args.plot
        Log.update()

        Main.update_folders(data_folder_path, plot_folder_path)
        Log.close_all_memory_handlers()

    @staticmethod
    @log.dump_args
    def update_folders(
        data_folder_path: str,
        plot_folder_path: str,
    ) -> None:
        """Update each folder"""

        folder_to_update: str

        folders_to_update: List[str] = AnalyzeFolders.get_folders_to_update(
            data_folder_path,
            plot_folder_path,
        )

        if folders_to_update:
            for folder_to_update in folders_to_update:
                Out.call_plot_tool(
                    data_folder_path,
                    plot_folder_path,
                    folder_to_update,
                )
                Out.copy_remark_file(
                    data_folder_path,
                    plot_folder_path,
                    folder_to_update,
                )
                Out.create_html_and_zip_file_for_plot_dir(
                    plot_folder_path,
                    folder_to_update,
                )
                Out.create_zip_file_for_data_dir(
                    data_folder_path,
                    plot_folder_path,
                    folder_to_update,
                )
                SCP.scp_dir_tree(
                    plot_folder_path,
                    folder_to_update,
                )


class Api(object):
    """API"""

    @staticmethod
    @log.dump_args
    def api(
        data_folder_path: Optional[str] = None,
        folder_to_update: Optional[str] = None,
    ) -> None:
        """Update one folder, called from external via this API."""
        if data_folder_path is None or folder_to_update is None:
            raise ValueError(f"needs {data_folder_path=} and {folder_to_update=}")

        Constant.data_folder_path = data_folder_path
        ApiConf.folder_to_update_api = folder_to_update

        Main.main()


if __name__ == "__main__":
    Main.main()
