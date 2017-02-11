import requests

URL = 'http://localhost/write'
USER = 'user'
PASSWORD = 'password'
DATABASE = 'database'
TIMEOUT_SECONDS = 5


def save_snapshot(points, test=False):
    payload = to_line_protol(points)
    if test:
        print '----- Test run (not saved) -----\n', payload
    else:
        query = {'db': DATABASE}
        res = requests.post(url=URL,
                            auth=(USER, PASSWORD),
                            params=query,
                            data=payload,
                            timeout=TIMEOUT_SECONDS)
        if not res.ok:
            print 'Error sending snapshot:', res.content


def to_line_protol(points):
    return '\n'.join([to_line(it) for it in points])


def to_line(point):
    (name, value) = point
    if isinstance(value, str):
        return '{} value="{}"'.format(name, value)
    elif isinstance(value, (int, float)):
        return '{} value={}'.format(name, str(value))
    else:
        raise Exception('Unsupported type for value: {}'.format(value))
