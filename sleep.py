from datetime import datetime, time
import asyncio


class Sleep:
    REMIND_TIMES = [
        "22:00", "22:30", "23:00", "23:30", "00:00", "00:15", "00:30", "00:45",
        "01:00", "01:10", "01:20", "01:30", "01:40", "01:50", "02:00"
    ]

    def __init__(self):
        """Precondition: this must be called before REMIND_TIMES[0]"""
        remind_times = [Sleep.parse_time(t) for t in Sleep.REMIND_TIMES]
        self._remind_times: list[time] = remind_times
        self._index = 0

    async def wait_until_next(self) -> None:
        now = datetime.now().time()
        later = self._remind_times[self._index]
        wait_seconds = Sleep.time_diff(later, now)
        print(f"Waiting {wait_seconds} seconds")
        self._index = (self._index + 1) % len(self._remind_times)
        await asyncio.sleep(wait_seconds)

    @staticmethod
    def parse_time(time_string: str) -> time:
        hours, minutes = time_string.split(":")
        return time(int(hours), int(minutes))

    @staticmethod
    def time_diff(time1: time, time2: time) -> int:
        """Return the number of seconds between two times.

        Precondition: time1 > time2

        >>> Sleep.time_diff(time(23), time(22))
        3600
        >>> Sleep.time_diff(time(0, 30), time(23))
        5400
        """
        t1 = time1.hour * 60 + time1.minute
        t2 = time2.hour * 60 + time2.minute
        return ((t1 - t2) % (24 * 60)) * 60


if __name__ == "__main__":
    import doctest
    doctest.testmod()
