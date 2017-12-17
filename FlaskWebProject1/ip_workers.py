from collections import namedtuple
from threading import Timer

VisitInfo = namedtuple("VisitInfo", "today_total unique_today total "
                                    "unique_total")


class IpTracker:
    def __init__(self):
        self.last_posted_ip = set()
        self.last_visited_ip = set()
        self.unique_ips = set()

    def track_ip(self, ip_from, posted, timeout=10):
        if posted:
            self.last_posted_ip.add(ip_from)
            Timer(timeout, lambda: self.last_posted_ip.remove(ip_from)).start()
        else:
            self.last_visited_ip.add(ip_from)
            Timer(timeout,
                  lambda: self.last_visited_ip.remove(ip_from)).start()

    def update_unique(self, ip):
        if ip not in self.unique_ips:
            self.unique_ips.add(ip)


class IpStorage:
    def __init__(self):
        self.today_total = 0
        self.unique_today = 0
        self.unique_total = 0
        self.total = 0

    def get_stats(self):
        return VisitInfo(self.today_total, self.unique_today, self.total,
                         self.unique_total)

    def flush(self):
        self.today_total = 0
        self.unique_today = 0

    def update(self, unique):
        if unique:
            self.unique_today += 1
            self.unique_total += 1
        self.today_total += 1
        self.total += 1
