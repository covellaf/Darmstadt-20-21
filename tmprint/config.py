#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

"""
# Setting config Variables.

Can be updated via the command line [argparser].

Note:
- if a '.env' file exists and does contain a line: 'MISSION = "xmm"'
'config.MISSION' will be updated.
- Same is true if an environment variable is set with 'MISSION = "xmm"'

## License
( c ) 2021 Nikolai von Krusenstiern, OPS-OAX
[MIT](https://gitlab.esa.int/xmmintfct/acc_patch/TMPrint/-/blob/develop/LICENSE)

## ToDo
- extend with pydantic, read .env
    - https://rednafi.github.io/digressions/python/2020/06/03/python-configs.html
    - https://betterprogramming.pub/the-beginners-guide-to-pydantic-ba33b26cde89
    - https://medium.com/swlh/cool-things-you-can-do-with-pydantic-fc1c948fbde0#f078
"""


from typing import List, Optional, Type

from pydantic import BaseModel, ValidationError, constr

from tmprint.constant import Constant


def main() -> None:
    """Main."""
    raise TypeError("'module' object is not callable")


# .env
MISSION_REGEX: str = r"(int|xmm)"
mission: Type[str] = constr(regex=MISSION_REGEX)

STATUS_REGEX: str = r"(DEV|OPS)"
status: Type[str] = constr(regex=STATUS_REGEX)


class Config(BaseModel):
    """
    Application configuration.
    """

    # .env
    MISSION: mission = Constant.DEFAULT_MISSION
    STATUS: status = Constant.DEFAULT_STATUS

    # Parer Arguments: Options
    list_plot_dirs: bool = False
    list_missing_plot_dirs: bool = False
    update_html_all: bool = False
    update_html: List[str] = []

    list_data_dirs: bool = False
    list_missing_data_dirs: bool = False
    plot_data_all: bool = False
    plot_data: List[str] = []


class ApiConf(object):
    """Special var for API call"""

    folder_to_update_api: Optional[str] = None


try:
    config = Config()
except ValidationError as err:
    print(err)


if __name__ == "__main__":
    main()
