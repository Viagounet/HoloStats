# Taken from : https://stackoverflow.com/questions/16742381/how-to-convert-youtube-api-duration-to-seconds
import re
import datetime


def YTDurationToSeconds(duration):
    match = re.match('PT(\d+H)?(\d+M)?(\d+S)?', duration).groups()
    hours = _js_parseInt(match[0]) if match[0] else 0
    minutes = _js_parseInt(match[1]) if match[1] else 0
    seconds = _js_parseInt(match[2]) if match[2] else 0
    return hours * 3600 + minutes * 60 + seconds


def yt_duration_to_datetime(duration):
    seconds = YTDurationToSeconds(duration)
    return datetime.timedelta(seconds=seconds)


# js-like parseInt
# https://gist.github.com/douglasmiranda/2174255
def _js_parseInt(string):
    return int(''.join([x for x in string if x.isdigit()]))
