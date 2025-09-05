import sys
from pathlib import Path
from typing import Any, Optional, TypeVar, cast

from loguru import Logger as LoguruLogger

# Define a type variable for the logger instance
LoggerType = TypeVar('LoggerType', bound='Logger')


class Logger:
    _instance: Optional['Logger'] = None
    _initialized: bool = False

    def __new__(cls: type[LoggerType], *args: Any, **kwargs: Any) -> 'Logger':
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        name: str = "app",
        log_level: str = "INFO",
        log_file: Optional[str] = None,
    ) -> None:
        """Initialize logger with console and optional file output.

        Args:
            name: Name of the logger
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional path to log file. If None, logs only to console.
        """
        if self._initialized:
            return

        self._logger = cast(LoguruLogger, logger)
        self._logger.remove()  # Remove default handler
        self._initialized = True

        # Validate log level
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        level = log_level.upper()
        if level not in valid_levels:
            raise ValueError(f"Invalid log level: {level}. Must be one of {valid_levels}")

        # Console handler
        self._add_console_handler(level)

        # File handler if log_file is provided
        if log_file is not None:
            self._add_file_handler(log_file, level)

    def _add_console_handler(self, level: str) -> None:
        """Add console handler to the logger."""
        self._logger.add(
            sys.stderr,
            format=(
                "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:"
                "<cyan>{line}</cyan> - <level>{message}</level>"
            ),
            level=level,
            colorize=True,
        )

    def _add_file_handler(self, log_file: str, level: str) -> None:
        """Add file handler to the logger.
        
        Args:
            log_file: Path to the log file
            level: Logging level
        """
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        self._logger.add(
            str(log_path),
            rotation="10 MB",
            retention="30 days",
            level=level,
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | "
                   "{level: <8} | "
                   "{name}:{function}:{line} - {message}",
            encoding="utf-8",
        )

    @property
    def logger(self) -> LoguruLogger:
        """Get the underlying loguru logger instance.
        
        Returns:
            LoguruLogger: Configured loguru logger instance
        """
        if not hasattr(self, '_logger') or self._logger is None:
            raise RuntimeError("Logger not initialized")
        return self._logger

    def get_logger(self) -> 'Logger':
        """Get the logger instance (for backward compatibility).
        
        Returns:
            Logger: The logger instance
        """
        return self

    def bind(self, **kwargs: Any) -> LoguruLogger:
        """Bind contextual values to the logger.
        
        Args:
            **kwargs: Key-value pairs to bind to the logger

        Returns:
            LoguruLogger: A new logger with the bound context
        """
        return self.logger.bind(**kwargs)

    def __call__(self, name: str = "app") -> LoguruLogger:
        """Allow using the logger as a callable to get a child logger.
        
        Args:
            name: Name for the child logger
            
        Returns:
            LoguruLogger: A new logger with the specified name
        """
        return self.bind(name=name)


# Create a default instance
logger = Logger()
