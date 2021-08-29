#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

"""
# Create html index.html file.

## License
( c ) 2021 Nikolai von Krusenstiern, OPS-OAX
[MIT](https://gitlab.esa.int/xmmintfct/acc_patch/TMPrint/-/blob/develop/LICENSE)
"""


import os
import pathlib
from typing import List, Optional, Tuple

import script_tools.log as log
from script_tools.log import Log
from script_tools.os_function import OsFunction
from tmprint.constant import Constant


def main() -> None:
    """Main."""
    raise TypeError("'module' object is not callable")


class HTML(object):
    """
    Create html index.html file.
    """

    h = f"h{Constant.HTML_HEADER_LEVEL}"

    @staticmethod
    @log.dump_args
    def create_file(
        plot_folder_path: str,
        folder_to_update: str,
        other_files_with_zip: List[str],
        png_files: List[str],
    ) -> None:
        """Create a index.html file for all files and plots in a directory."""
        now_date_time_utc: str
        time_plot_updated: str

        folder_to_update_path: str = os.path.join(plot_folder_path, folder_to_update)
        index_file_path: str = os.path.join(
            folder_to_update_path,
            Constant.INDEX_FILE_NAME,
        )
        remark_file_path: str = os.path.join(
            folder_to_update_path,
            Constant.REMARK_FILE_NAME,
        )

        other_files_with_zip = sorted(other_files_with_zip)
        png_file: Optional[str]
        if not png_files:
            png_file = None
        else:
            png_file = png_files[0]
            png_files = sorted(png_files)

        now_date_time_utc, time_plot_updated = HTML.get_dates(
            plot_folder_path,
            folder_to_update,
            png_file,
        )

        Log.debug(f"Create {Constant.INDEX_FILE_NAME} for {folder_to_update=}")
        Log.debug(f"{index_file_path=}", level=Log.LOG_DICT["VAR"])

        with open(index_file_path, "w") as file_handle:
            file_handle.write(HTML.render_header())
            file_handle.write(
                HTML.render_back_to_and_dates(now_date_time_utc, time_plot_updated),
            )

            # NvK: Feature Request TG
            if OsFunction.file_exists(remark_file_path):
                Log.debug(
                    f"in-lining {remark_file_path=}",
                    level=Log.LOG_DICT["DEBUG2"],
                )
                file_handle.write(HTML.render_remark(remark_file_path))

            for file_ in other_files_with_zip:
                file_handle.write(HTML.render_file_item(file_))

            for file_ in png_files:
                file_handle.write(HTML.render_png_item(file_))

            file_handle.write(HTML.render_footer())

    @staticmethod
    @log.dump_args
    def get_dates(
        folder_path: str,
        folder_to_update: str,
        file_name: Optional[str] = None,
    ) -> Tuple[str, str]:
        """Get dates for last plot generation as well as now."""

        if file_name is None:
            time_plot_updated = "No png files generated."
        else:
            file_path_str: str = os.path.join(folder_path, folder_to_update)
            file_path_str = os.path.join(file_path_str, file_name)
            file_path = pathlib.Path(file_path_str)
            time_plot_updated = OsFunction.get_last_update_time_of_file(file_path)

        now_date_time_utc = OsFunction.get_time_stamp_in_utc()

        return now_date_time_utc, time_plot_updated

    @staticmethod
    @log.dump_args
    def render_header() -> str:
        """Return html header."""
        html_header: str = """
            <html>
                <body>
            """
        return html_header

    @staticmethod
    @log.dump_args
    def render_back_to_and_dates(time_stamp_html, time_stamp_plots) -> str:
        """
        Render a link to Return back to rhe calling php.
        And as well as insert the current time stamp.
        """
        html_back_to: str = f"""
            <{HTML.h}>
                <a href='/{Constant.REMOTE_PHP}'>Back to directory</a>
            </{HTML.h}>
                Last updates:
                <ul>
                <li>plots: {time_stamp_plots}</li>
                <li>html: {time_stamp_html}</li>
                </ul>
            <hr />
        """
        return html_back_to

    @staticmethod
    @log.dump_args
    def render_remark(file_: str) -> str:
        """Add user remarks to index.html from remark.html file, if any."""
        with open(file_, "r") as file_handler:
            html_of_remark = file_handler.read()
            html_of_remark = f"""
                {html_of_remark}
                <hr />
                """
            return html_of_remark

    @staticmethod
    @log.dump_args
    def render_footer() -> str:
        """Return html footer."""
        html_footer: str = """
                </body>
            </html>
            """
        return html_footer

    @staticmethod
    @log.dump_args
    def render_file_item(file_: str) -> str:
        """Return a html list entry for a file."""
        html_file_item: str = f"""
            <{HTML.h}>
                <a href='{file_}'>{file_}</a>
            </{HTML.h}>
            """
        return html_file_item

    @staticmethod
    @log.dump_args
    def render_png_item(file_: str) -> str:
        """Return a html link to an inline image."""
        html_png_item: str = f"""
            <{HTML.h}>
                {file_}
            </{HTML.h}>
            <img src='{file_}'/>
            """
        return html_png_item


if __name__ == "__main__":
    main()
