#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

"""
#  Setting Constant Variables.

## License
( c ) 2021 Nikolai von Krusenstiern, OPS-OAX
[MIT](https://gitlab.esa.int/xmmintfct/acc_patch/TMPrint/-/blob/develop/LICENSE)
"""


import os
import sys
import zipfile
from typing import List, Optional


def main() -> None:
    """Main."""
    raise TypeError("'module' object is not callable")


class Constant(object):
    """
    Setting Constant Variables.
    """

    # DEV
    CALL_SCRIPT_FROM_CRON: bool = False
    CALL_SCRIPT_NO_FILTER: bool = True

    # Fallback
    DEFAULT_MISSION: str = "int"  # or "xmm"
    DEFAULT_STATUS: str = "OPS"  # or "DEV"

    # Meta
    SCRIPT_FILE: str = os.path.basename(sys.argv[0])
    SCRIPT_NAME: str = os.path.splitext(SCRIPT_FILE)[0]
    SCRIPT_ARGV: List[str] = sys.argv[1:]

    # Zip Compression
    COMPRESSION: int = zipfile.ZIP_DEFLATED

    # datetime format
    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%SZ"

    # Working folders
    DATA_FOLDER_NAME: str = "SLW_DATA"
    PLOT_FOLDER_NAME: str = "SLW_PLOTS"
    WORK_FOLDER_PATH: str = "/home/imcsuser/TMPrint"

    data_folder_path: str = os.path.join(
        WORK_FOLDER_PATH,
        DATA_FOLDER_NAME,
    )
    plot_folder_path: str = os.path.join(
        WORK_FOLDER_PATH,
        PLOT_FOLDER_NAME,
    )

    # HTML out
    INDEX_FILE_NAME: str = "index.html"
    REMARK_FILE_NAME: str = "remark.html"
    HTML_HEADER_LEVEL: int = 3

    # Web Server
    REMOTE_USER: str = "webadmin"
    REMOTE_HOST: str = "xmm.esoc.esa.int"

    _REMOTE_PATH: str = "/home/webadmin/htdocs/docs/simulations"
    _REMOTE_PHP_PATH: str = "documentation"
    _REMOTE_PHP_STUB: str = "sim_tests.php"

    REMOTE_PHP: Optional[str] = None
    REMOTE_PATH: Optional[str] = None
    REMOTE_URL: Optional[str] = None

    @staticmethod
    def make_specific_for(mission: str) -> None:
        """Make mission specific Constant variables"""

        remote_php_file: str = f"{mission}_{Constant._REMOTE_PHP_STUB}"

        Constant.REMOTE_PATH = os.path.join(Constant._REMOTE_PATH, mission)
        Constant.REMOTE_PHP = os.path.join(Constant._REMOTE_PHP_PATH, remote_php_file)
        Constant.REMOTE_URL = f"http://{Constant.REMOTE_HOST}/{Constant.REMOTE_PHP}"

    @staticmethod
    def setup(mission: Optional[str] = None) -> None:
        """Update Constant"""
        if mission is None:
            mission = str(Constant.DEFAULT_MISSION)
        Constant.make_specific_for(mission)


if __name__ == "__main__":
    main()
