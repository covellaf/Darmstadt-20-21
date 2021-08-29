#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

"""
#  Provide logging.

## License
( c ) 2021 Nikolai von Krusenstiern, OPS-OAX
[MIT](https://gitlab.esa.int/xmmintfct/acc_patch/TMPrint/-/blob/develop/LICENSE)
"""


import contextlib
import inspect
import logging
import logging.handlers
import time
from pprint import pprint
from typing import Any, Callable, Dict, Optional, OrderedDict, TextIO, Tuple

from script_tools.tools import Tools
from tmprint.config import config
from tmprint.constant import Constant


def main() -> None:
    """Main."""
    raise TypeError("'module' object is not callable")


def dump_args(func: Callable[..., Any]):
    """
    Decorator to print function call details.

    This includes parameters names and effective values.

    From: https://stackoverflow.com/questions/6200270/decorator-that-prints-function-call-details-parameters-names-and-effective-valu  # noqa: E501, B950
    Remark: Not completely type annotated.
    """

    def wrapper(*args, **kwargs) -> Callable[..., Any]:
        if Log.console_level <= Log.LOG_DICT["FUNCTION"]:
            func_args: OrderedDict[str, Any] = (
                inspect.signature(func).bind(*args, **kwargs).arguments
            )
            func_args_str: str = ", ".join(
                "{} = {!r}".format(*item) for item in func_args.items()
            )
            Log.debug(
                f"{func.__module__}.{func.__qualname__} ( {func_args_str} )",
                level=Log.LOG_DICT["FUNCTION"],
            )
            Log.debug_halt()
        return func(*args, **kwargs)

    return wrapper


class Log(object):
    """
    Provide logging.
    """

    LOG_DICT: Dict[str, int] = {
        "CRITICAL": 50,
        "ERROR": 40,
        "WARNING": 30,
        "INFO": 20,
        "DEBUG": 10,
        "DEBUG2": 9,
        "EXTERNAL": 8,
        "VAR": 7,
        "FUNCTION": 5,
        "STDOUT": 4,
        "LOOP": 3,
        "ALL": 1,
        "NOTSET": 0,
    }
    console_level: int = LOG_DICT["WARNING"]

    LOG_FILE_LEVEL: int = LOG_DICT["ERROR"]
    MEMORY_LEVEL: int = LOG_DICT["FUNCTION"]
    LOG_LINES: int = 4096

    VERBOSE: bool = console_level <= LOG_DICT["INFO"]
    DEBUG: int = 1 if console_level <= LOG_DICT["DEBUG"] else 0
    DEBUG_HALT: bool = False

    logger: logging.Logger
    formatter: logging.Formatter

    log_file: logging.Handler
    console: logging.Handler
    memory: logging.Handler
    null: logging.Handler

    @staticmethod
    @dump_args
    def setup(
        logger_name: Optional[str] = None,
    ) -> None:
        """Setup logging."""
        if logger_name is None:
            logger_name = __name__

        logger: logging.Logger
        formatter: logging.Formatter

        logger, formatter = Log.setup_logger(logger_name)
        Log.add_level_names()

        file_handler: logging.FileHandler = Log.setup_file_logger(
            logger_name,
            logger,
            formatter,
        )

        console_handler: logging.StreamHandler = Log.setup_console_logger(
            logger,
            formatter,
        )

        memory_handler: logging.handlers.MemoryHandler = Log.setup_memory_logger(
            logger,
            formatter,
            file_handler,
        )

        null_handler: logging.NullHandler = Log.setup_null_logger(
            logger,
        )

        Log.logger = logger
        Log.formatter = formatter

        Log.log_file = file_handler
        Log.console = console_handler
        Log.memory = memory_handler
        Log.null = null_handler

    @staticmethod
    @dump_args
    def setup_logger(
        logger_name: str,
    ) -> Tuple[logging.Logger, logging.Formatter]:
        """Setup logger."""

        logger: logging.Logger = logging.getLogger(logger_name)
        logger.setLevel(Log.LOG_DICT["ALL"])
        logging.Formatter.converter = time.gmtime
        formatter: logging.Formatter = logging.Formatter(
            "%(asctime)s %(name)s [%(levelno)02d %(levelname)s] %(message)s",
        )

        return logger, formatter

    @staticmethod
    @dump_args
    def add_level_names() -> None:
        """Add level names to logger."""
        level_name: str
        level: int

        for level_name, level in Log.LOG_DICT.items():
            if (level % 10) != 0:
                logging.addLevelName(level, level_name)

    @staticmethod
    @dump_args
    def setup_console_logger(
        logger: logging.Logger,
        formatter: logging.Formatter,
    ) -> logging.StreamHandler:
        """Setup console logger."""

        console_handler: logging.StreamHandler = logging.StreamHandler()
        console_handler.setLevel(Log.console_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return console_handler

    @staticmethod
    @dump_args
    def setup_file_logger(
        logger_name: str,
        logger: logging.Logger,
        formatter: logging.Formatter,
    ) -> logging.FileHandler:
        """Setup file logger."""
        file_handler: logging.FileHandler = logging.handlers.RotatingFileHandler(
            f"{logger_name}.log",
            maxBytes=10 ** 5,
            backupCount=1,
        )
        file_handler.setLevel(Log.LOG_FILE_LEVEL)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return file_handler

    @staticmethod
    @dump_args
    def setup_memory_logger(
        logger: logging.Logger,
        formatter: logging.Formatter,
        target: logging.Handler,
    ) -> logging.handlers.MemoryHandler:
        """Setup memory logger."""
        memory_handler: logging.handlers.MemoryHandler = logging.handlers.MemoryHandler(
            capacity=Log.LOG_LINES,
            flushLevel=Log.LOG_DICT["ERROR"],
            target=target,
            flushOnClose=True,
        )
        memory_handler.setLevel(Log.MEMORY_LEVEL)
        memory_handler.setFormatter(formatter)
        logger.addHandler(memory_handler)

        return memory_handler

    @staticmethod
    @dump_args
    def setup_null_logger(logger: logging.Logger) -> logging.NullHandler:
        """Setup NULL logger."""
        null_handler: logging.NullHandler = logging.NullHandler()
        logger.addHandler(null_handler)
        return null_handler

    @staticmethod
    def debug(line: str, level: Optional[int] = None) -> None:
        """Debug output."""
        standard: int = Log.LOG_DICT["DEBUG"]
        level = standard if level is None else level

        if not (standard - 10) < level <= standard:
            level_str: str = Tools.get_key_for_value(Log.LOG_DICT, standard)
            raise ValueError(
                f"log level for {level_str} out of range: {level=}.",
            )
        Log.logger.log(level, line)

    @staticmethod
    def debug_halt() -> None:
        """Halt after debug message."""
        if Log.DEBUG_HALT:
            input("Press RETURN to continue...")

    @staticmethod
    @dump_args
    def update():
        """Update info for log."""
        Log.logger.info(f"{Constant.SCRIPT_FILE} {Constant.SCRIPT_ARGV}")
        if Log.console_level <= Log.LOG_DICT["VAR"]:
            pprint(vars(Constant), sort_dicts=True)
            pprint(vars(config), sort_dicts=True)

    @staticmethod
    @dump_args
    def close_all_memory_handlers():
        """
        Close logging memory handlers.
        """
        for handler in Log.logger.handlers:
            if isinstance(handler, logging.handlers.MemoryHandler):
                handler.setTarget(Log.null)
                handler.close()


class StdOutErrLogger:
    """
    A context manager to redirect stdout to logger.
    """

    def __init__(
        self,
        logger: logging.Logger,
        level: int = Log.LOG_DICT["VAR"],
        redirect: TextIO = contextlib.redirect_stdout,
    ):
        self.logger = logger
        self.name = self.logger.name
        self.level = level
        self._redirector = redirect(self)

    def write(self, msg):
        """Write stdout to log."""
        if msg and not msg.isspace():
            self.logger.log(self.level, msg)

    def flush(self):
        """Dummy flash method, for compatibility."""
        self.logger.warning("'%s.flush()' not implemented.", self.name)

    def __enter__(self):
        self._redirector.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # let contextlib do any exception handling here
        self._redirector.__exit__(exc_type, exc_value, traceback)


if __name__ == "__main__":
    main()
