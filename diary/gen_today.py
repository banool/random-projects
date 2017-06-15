#!/usr/bin/env python3.6

from contextlib import suppress
from datetime import datetime, timedelta
from os import mkdir
from tools import (
    get_config,
    fancy_date_string,
    seconds_since_midnight,
)

import os.path
import subprocess
import time

config = get_config()
local_tz = config['LOCAL_TZ']


def get_entry_date():
    '''
    If you're writing the diary entry after midnight, you're probably writing
    for what happened in technically the previous day. This function confirms
    which date you actually want to write the entry for.
    '''
    today_fancy = fancy_date_string(local_tz, day_offset=0)
    fancy = today_fancy
    day_offset = 0
    current_unix_time = int(time.time())
    secs_since_midnight = seconds_since_midnight()
    print(f'The current date is {today_fancy}.')
    if secs_since_midnight < 72000:  # 18000 == 5am, but just making it big because i wanna be asked always
        yesterday_fancy = fancy_date_string(local_tz, day_offset=-1)
        print(f'Are you sure you don\'t mean {yesterday_fancy}?')
        response = None
        while response not in [1, 2, 3]:
            with suppress(ValueError):
                response = int(input(
                    f'[1] This entry is for {today_fancy}.\n'
                    f'[2] This entry is for {yesterday_fancy}.\n'
                    f'[3] This entry is for another date.\n'
                    f'Please choose one of the above: '
                ))
        # For response 1 and 2 we get the unix time at noon for that day.
        if response == 1:
            pass
        elif response == 2:
            fancy = yesterday_fancy
            day_offset = -1
        else:
            conf = False
            while not conf:
                day_offset = -(int(input('How many days ago do you want? ')))
                fancy = fancy_date_string(local_tz, day_offset=day_offset)
                print('Is this the date you mean:')
                print(fancy)
                response = input('Enter (y)es or (n)o: ')
                if response[0].lower() == 'y':
                    conf = True

    unix_time = current_unix_time - secs_since_midnight + \
        43200 - (86400 * -day_offset)

    return (fancy, day_offset, unix_time)


date_fancy, day_offset, unix_time_at_noon = get_entry_date()

structure = [
    ['# ', date_fancy],
    [''],
    # I guess just put things that you watched or read or whatever
    ['## Media consumed'],
    ['Started: '],
    ['Continued: '],
    ['Finished: '],
    [''],
    # You don't have to fill this section in if nothing happened friend :)
    ['## Life events'],
    [''],
    # The tags should be comma separated.
    ['## Indexing metadata'],
    ['Tags: '],
    # These are the people who feature in the diary entry.
    ['People: '],
    [''],
    ['## Time metadata'],
    ['Local date with timezone: ', date_fancy],
    # The unix time field is the unix time for the day that the entry
    # is being written about. The time represents when I woke up, not when the
    # diary entry was written, just in case I wrote the entry after midnight.
    ['Unix time at noon: ', str(unix_time_at_noon)],
    ['Local TZ: ', local_tz],
    [''],
]

ENTRIES_DIRECTORY_NAME = 'entries'
if not os.path.isdir(ENTRIES_DIRECTORY_NAME):
    mkdir(ENTRIES_DIRECTORY_NAME)

dt = datetime.today() - timedelta(-day_offset)
fname = os.path.join(ENTRIES_DIRECTORY_NAME, f'{dt.year}-{dt:%m}-{dt:%d}.md')
if not os.path.isfile(fname):
    with open(fname, 'w') as f:
        f.writelines([''.join(line) + '\n' for line in structure])
else:
    print(f'The file name {fname} already exists. Chickening out.')

for editor in ['code', 'atom -a']:
    with suppress(subprocess.CalledProcessError):
        subprocess.check_output(
            f'{editor} {fname}',
            shell=True,
            stderr=subprocess.DEVNULL,
        )
        break
