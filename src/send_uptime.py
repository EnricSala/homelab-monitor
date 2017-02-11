import re
from repository import save_snapshot

CPU_THREAD_COUNT = 8


def parse_uptime(string):
    # Get uptime
    uptime = re.search(r"up +(.+?),", string).group(1)
    uptime = ('server.uptime', uptime)

    # Get online user amount
    users = int(re.search(r", +(\d+) user", string).group(1))
    users = ('server.users.online', users)

    # Get load averages for 1, 5, 15 min
    loads = [it.group(0) for it in re.finditer(r"(\d+[,\.]\d+)", string)]
    loads = [float(it.replace(',', '.')) for it in loads]
    loads = [it * 100 / CPU_THREAD_COUNT for it in loads]
    names = ['server.load.1min', 'server.load.5min', 'server.load.15min']
    loads = zip(names, loads)

    # Build measurements
    return [uptime, users] + loads


with open('../samples/uptime_v1.txt', 'r') as myfile:
    stdin = myfile.read()

points = parse_uptime(stdin)
save_snapshot(points, test=True)
