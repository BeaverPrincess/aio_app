import logging


class AppLogger:
    def __init__(self, verbose: bool = False) -> None:
        self._verbose = verbose
        self._logger = logging.getLogger(
            f"{self.__class__.__module__}.{self.__class__.__qualname__}"
        )

    def debug(self, message: str) -> None:
        if self._verbose:
            self._logger.debug(message)

    def info(self, message: str) -> None:
        if self._verbose:
            self._logger.info(message)

    def warning(self, message: str) -> None:
        if self._verbose:
            self._logger.warning(message)

    def error(self, message: str) -> None:
        self._logger.error(message)
