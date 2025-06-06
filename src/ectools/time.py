import datetime

default_time_format: str = "%Y%m%d-%H:%M:%S"
# default_time_format_long: str = "%Y%m%d-%H:%M:%S:%f"
# default_time_format_short: str = "%Y%m%d_%H%M%S"


def time_now_str(fmt: str | None = None) -> str:
    if fmt is None:
        fmt = default_time_format
    return datetime.datetime.now().strftime(fmt)


def time_now_filing() -> str:
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S%f")[:-3]  # Trim to milliseconds
