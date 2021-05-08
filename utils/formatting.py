from datetime import timedelta


def format_label(value: int, one_label: str, many_label: str) -> str:
    assert value > 0

    if value == 1:
        return f'{value} {one_label}'

    return f'{value} {many_label}'


def format_delta(delta: timedelta) -> str:
    time = int(delta.total_seconds())

    if time < 1:
        return '<1 second'

    if time < 60:
        return format_label(time, 'second', 'seconds')

    time = time // 60
    if time < 60:
        return format_label(time, 'minute', 'minutes')

    time = time // 60
    if time < 60:
        return format_label(time, 'hour', 'hours')

    time //= 24
    if time < 24:
        return format_label(time, 'day', 'days')

    time //= 30
    if time < 30:
        return format_label(time, 'month', 'months')

    time //= 12
    return format_label(time, 'year', 'years')