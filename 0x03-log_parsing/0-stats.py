#!/usr/bin/python3
"""
Log parsing script that reads stdin line by line and computes metrics.

Input format: <IP Address> - [<date>] "GET /projects/260 HTTP/1.1" <status code> <file size>
(if the format is not this one, the line must be skipped)
After every 10 lines and/or a keyboard interruption (CTRL + C), print these statistics from the beginning:
Total file size: File size: <total size>
Number of lines by status code:
possible status code: 200, 301, 400, 401, 403, 404, 405, 500
if a status code doesn’t appear or is not an integer, don’t print anything for this status code
format: <status code>: <number>
status codes should be printed in ascending order
"""

import sys
import signal

# Store the count of all status codes in a dictionary
status_codes_dict = {'200': 0, '301': 0, '400': 0, '401': 0, '403': 0, '404': 0, '405': 0, '500': 0}
total_size = 0
count = 0  # Keep count of the number of lines counted

def print_stats():
    """Print statistics"""
    print('File size: {}'.format(total_size))
    for key in sorted(status_codes_dict.keys()):
        if status_codes_dict[key] > 0:
            print('{}: {}'.format(key, status_codes_dict[key]))

def signal_handler(sig, frame):
    """Handle keyboard interruption"""
    print_stats()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

try:
    for line in sys.stdin:
        parts = line.split()
        if len(parts) < 9:
            continue

        status_code = parts[-2]
        file_size = parts[-1]

        try:
            file_size = int(file_size)
            total_size += file_size
        except ValueError:
            continue

        if status_code in status_codes_dict:
            status_codes_dict[status_code] += 1

        count += 1

        if count == 10:
            print_stats()
            count = 0

except Exception as err:
    pass
finally:
    print_stats()
