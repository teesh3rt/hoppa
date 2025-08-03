import inspect
from globals import DEBUGGING_ENABLED

GRAY = "90"
RED = "31"
GREEN = "32"
YELLOW = "33"
BLUE = "34"
MAGENTA = "35"
CYAN = "36"


def generate_logger(name: str, color: str, conditional: bool = True):
    def logger(*args, context=None, **kwargs):
        caller_frame = inspect.currentframe().f_back
        caller_file = caller_frame.f_code.co_filename
        caller_line = caller_frame.f_lineno
        if context is None:
            context = f"{caller_file}:{caller_line}"
        else:
            context = f"{context} ({caller_file}:{caller_line})"
        print(
            f"\033[{color}m{name}\033[0m",
            f"\033[{GRAY}m{context}\033[0m",
            *args,
            **kwargs,
        )

    def empty(*args, **kwargs):
        pass

    if conditional:
        return logger
    else:
        return empty


info = generate_logger("info", GREEN)
debug = generate_logger("debug", BLUE, DEBUGGING_ENABLED)
warn = generate_logger("warn", YELLOW)
error = generate_logger("error", RED)
fatal = generate_logger("fatal", MAGENTA)
