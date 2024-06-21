import re


def valid_times(mailing_times: str) -> list:  # нужно адекватно написать
    pattern = r"\d\d:\d\d"
    lst = re.findall(pattern, mailing_times)
    if lst:
        for time_ in lst:
            hours, minutes = time_.split(":")
            if 0 <= int(hours) <= 24 and 0 <= int(minutes) <= 60:
                continue
            else:
                return []
        return lst
    return []
