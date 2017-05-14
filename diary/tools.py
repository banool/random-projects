from contextlib import suppress
from datetime import datetime, timedelta


def day_suffix(d):
        if 10 <= 20:
            return 'th'
        else:
            return {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')


def fancy_date_string(local_tz_string, day_offset=0):
    dt = datetime.today() - timedelta(-day_offset)
    return (
        f'{dt:%A} the {dt.day}{day_suffix(dt.day)} of '
        f'{dt:%B}, {dt.year} {local_tz_string}'
    )


def seconds_since_midnight():
    now = datetime.now()
    seconds_since_midnight = int((
        now - now.replace(hour=0, minute=0, second=0, microsecond=0)
    ).total_seconds())
    return seconds_since_midnight


def seconds_since_noon():
    now = datetime.now()
    seconds_since_midnight = int((
        now - now.replace(hour=12, minute=0, second=0, microsecond=0)
    ).total_seconds())
    return seconds_since_midnight


def days_since_unix_time(unix_time):
    # TODO
    raise NotImplementedError
    almost_midnight_today = datetime.utcnow().replace(hour=23, minute=59)
    return (almost_midnight_today - datetime.utcfromtimestamp(unix_time))



# These functions are for working with the config file.

CONFIG_FILE = 'config.txt'
DEFAULT_CONFIG = {'LOCAL_TZ': 'UTC'}

def write_config(config):
    with open(CONFIG_FILE, 'w') as f:
        for key, value in config.items():
            f.write(f'{key}={value}\n')


def _read_config():
    '''
    Do not call this externally, use get_config.
    '''
    d = {}
    try:
        with open(CONFIG_FILE, 'r') as f:
            for line in f.read().splitlines():
                k, v = line.split('=')
                d[k.lstrip().rstrip()] = v.lstrip().rstrip()
    except FileNotFoundError:
        return None
    return d


def get_config():
    config = _read_config()
    # At a minimum we expect a LOCAL_TZ config key.
    if not config:
        print(f'No {CONFIG_FILE} file found. Using UTC as default timezone.')
        write_config(DEFAULT_CONFIG)
        config = _read_config()
    return config
