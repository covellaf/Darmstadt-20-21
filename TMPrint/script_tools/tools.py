#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

"""
#  Tools are a collection of convenience methods.

## License
( c ) 2021 Nikolai von Krusenstiern, OPS-OAX
[MIT](https://gitlab.esa.int/xmmintfct/acc_patch/TMPrint/-/blob/develop/LICENSE)
"""


from typing import Any, Dict


def main() -> None:
    """Main."""
    raise TypeError("'module' object is not callable")


class Tools(object):
    """
    Tools are a collection of convenience methods.
    """

    @staticmethod
    def get_key_for_value(dict_: Dict[Any, Any], value: Any) -> Any:
        """get the dict key from a value"""
        key_list = list(dict_.keys())
        val_list = list(dict_.values())
        position = val_list.index(value)
        key_for_value = key_list[position]
        return key_for_value


if __name__ == "__main__":
    main()
