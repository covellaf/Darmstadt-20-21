#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

"""
# scp files to remote host.

## License
( c ) 2021 Nikolai von Krusenstiern, OPS-OAX
[MIT](https://gitlab.esa.int/xmmintfct/acc_patch/TMPrint/-/blob/develop/LICENSE)
"""


import os
import socket
import sys
from typing import Optional

import script_tools.log as log
from script_tools.log import Log
from script_tools.os_function import OsFunction
from tmprint.constant import Constant


def main() -> None:
    """Main."""
    raise TypeError("'module' object is not callable")


class SCP(object):
    """
    scp files to remote host.
    """

    @staticmethod
    @log.dump_args
    def ssh_port_is_closed(remote_host: str, port: Optional[int] = None) -> int:
        """Check if INET port is open/closed."""
        port = 22 if port is None else port

        socket_: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssh_port_status: int = socket_.connect_ex((remote_host, port))
        return ssh_port_status

    @staticmethod
    @log.dump_args
    def scp_dir_tree(
        path: str,
        folder: str,
        remote_user: Optional[str] = None,
        remote_host: Optional[str] = None,
        remote_path: Optional[str] = None,
    ) -> None:
        """scp a directory tree."""

        if remote_user is None:
            remote_user = Constant.REMOTE_USER
        if remote_host is None:
            remote_host = Constant.REMOTE_HOST
        if remote_path is None:
            remote_path = Constant.REMOTE_PATH

        remote_url: str = f"{remote_user}@{remote_host}:{remote_path}/"
        source_path: str = os.path.join(path, folder)

        if not OsFunction.dir_exists(source_path):
            Log.logger.warning(
                f"Can not scp dir tree since '{source_path}' is not a dir.",
            )
            sys.exit(1)

        if not SCP.ssh_port_is_closed(remote_host):
            Log.debug(f"scp {folder=} to {remote_host=}")
            Log.debug(f"to: {remote_url=}", level=Log.LOG_DICT["VAR"])

            os_call: str = f"scp -q -r {source_path} {remote_url}"
            Log.debug(f"call: {os_call}", level=Log.LOG_DICT["EXTERNAL"])
            os.system(os_call)
        else:
            Log.logger.warning(f"SCP: could not connect to {remote_host}")


if __name__ == "__main__":
    main()
