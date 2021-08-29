#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

"""
#  Parsing cmd line arguments, if any.

## License
( c ) 2021 Nikolai von Krusenstiern, OPS-OAX
[MIT](https://gitlab.esa.int/xmmintfct/acc_patch/TMPrint/-/blob/develop/LICENSE)
"""


import argparse

import script_tools.log as log
from script_tools.log import Log
from script_tools.os_function import OsFunction
from tmprint.config import config
from tmprint.constant import Constant


def main() -> None:
    """Main."""
    raise TypeError("'module' object is not callable")


class Parser(object):
    """
    Parsing cmd line arguments, if any.
    """

    parser: argparse.ArgumentParser

    @staticmethod
    @log.dump_args
    def parse() -> argparse.Namespace:
        """Configure Parser and parse."""
        args: argparse.Namespace = Parser.argparser()
        Parser.validate(args)
        Parser.set_globals(args)
        return args

    @staticmethod
    @log.dump_args
    def argparser() -> argparse.Namespace:
        """Configure Parser."""

        class CustomFormatter(
            argparse.ArgumentDefaultsHelpFormatter,
            argparse.RawDescriptionHelpFormatter,
        ):
            """
            Multiple inheritance, to use both formatter classes.
            """

        parser: argparse.ArgumentParser = argparse.ArgumentParser(
            formatter_class=CustomFormatter,
            description=f"""\
{Constant.SCRIPT_FILE}: SIM Tests - Create plots, html and zip files and sync to web server.
Standard usage: Without arguments, will create and populate missing plot directories and sync to web server.
""",  # noqa: E501, B950
            epilog=f"""\
  --DEBUG --DEBUG --DEBUG       set DEBUG level 3, ...
Destination: {Constant.REMOTE_URL}
""",
        )

        plots = parser.add_mutually_exclusive_group()
        html = parser.add_mutually_exclusive_group()
        lists = parser.add_mutually_exclusive_group()
        logs = parser.add_mutually_exclusive_group()

        parser.add_argument(
            "--data",
            default=Constant.data_folder_path,
            help="set data folder",
        )
        parser.add_argument(
            "--plot",
            default=Constant.plot_folder_path,
            help="set plot folder",
        )

        plots.add_argument(
            "--PLOT-DATA-ALL",
            default=config.plot_data_all,
            help="compute plots for all folders. [Will over-write.]",
            action="store_true",
        )
        plots.add_argument(
            "--PLOT-DATA",
            default=config.plot_data,
            help="compute plots for named folders. [Will over-write.]",
            nargs="*",
        )

        html.add_argument(
            "--update-html-all",
            default=config.update_html_all,
            help="update html and zip file for all plot folders and upload to server",
            action="store_true",
        )
        html.add_argument(
            "--update-html",
            default=config.update_html,
            help="update html and zip file for named folders and upload to server",
            nargs="*",
        )

        lists.add_argument(
            "--list-data-dirs",
            default=config.list_data_dirs,
            help="list sim test sub-dirs in DATA folder",
            action="store_true",
        )
        lists.add_argument(
            "--list-plot-dirs",
            default=config.list_plot_dirs,
            help="list sim tests sub-dirs in PLOT folder",
            action="store_true",
        )
        lists.add_argument(
            "--list-missing-data-dirs",
            default=config.list_missing_data_dirs,
            help="list sub-dirs in PLOT folder, which are missing in the DATA folder",
            action="store_true",
        )
        lists.add_argument(
            "--list-missing-plot-dirs",
            default=config.list_missing_plot_dirs,
            help="list sub-dirs in DATA folder, which are missing in the PLOT folder",
            action="store_true",
        )

        logs.add_argument(
            "--verbose",
            default=Log.VERBOSE,
            help="set verbose mode",
            action="store_true",
        )
        logs.add_argument(
            "--DEBUG",
            default=Log.DEBUG,
            help="set DEBUG level",
            action="count",
        )

        Parser.parser = parser

        args: argparse.Namespace = parser.parse_args()
        Log.debug(f"{args=}")
        return args

    @staticmethod
    @log.dump_args
    def set_globals(args: argparse.Namespace) -> None:
        """Set Globals."""

        config.list_data_dirs = args.list_data_dirs
        config.list_plot_dirs = args.list_plot_dirs

        config.list_missing_data_dirs = args.list_missing_data_dirs
        config.list_missing_plot_dirs = args.list_missing_plot_dirs

        config.plot_data = args.PLOT_DATA
        config.plot_data_all = args.PLOT_DATA_ALL

        config.update_html = args.update_html
        config.update_html_all = args.update_html_all

        if args.verbose:
            Log.console_level = min(
                Log.console_level,
                Log.LOG_DICT["INFO"],
            )

        if args.DEBUG:
            Log.console_level = min(
                Log.console_level,
                Log.LOG_DICT["DEBUG"] + 1 - args.DEBUG,
            )

        Log.console.setLevel(Log.console_level)
        Log.debug(f"{Log.console_level=}", level=Log.LOG_DICT["VAR"])

    @staticmethod
    @log.dump_args
    def validate(args: argparse.Namespace) -> None:
        """Validate parser arguments."""
        path: str

        for path in (args.data, args.plot):
            OsFunction.dir_exists_or_exit(path)

        if args.update_html:
            OsFunction.sub_dirs_exist_or_exit(args.plot, args.update_html)

        if args.PLOT_DATA:
            OsFunction.sub_dirs_exist_or_exit(args.data, args.PLOT_DATA)


if __name__ == "__main__":
    main()
