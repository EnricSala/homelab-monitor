import re
import command_executor as executor
import influxdb_repository as repository

DEVICES = [
    ('acpitz-virtual-0', [
        ('temp1', 'motherboard.sensor1.temperature'),
        ('temp2', 'motherboard.sensor2.temperature')
    ]),
    ('coretemp-isa-0000', [
        ('Physical id 0', 'cpu.chipset.temperature'),
        ('Core 0', 'cpu.core1.temperature'),
        ('Core 1', 'cpu.core2.temperature'),
        ('Core 2', 'cpu.core3.temperature'),
        ('Core 3', 'cpu.core4.temperature')
    ])
]


def parse_sensors(devices, string):
    result = []
    for dev in devices:
        sensors = parse_device(dev, string)
        result.extend(sensors)
    return result


def parse_device(device, string):
    (name, sensor_attrs) = device
    exp = r"^({}.*?)\n\n".format(re.escape(name))
    match = re.search(exp, string, flags=re.MULTILINE | re.DOTALL)
    if match:
        substr = match.group(1)
        return parse_attrs(substr, sensor_attrs)
    else:
        print 'Cannot find device:', name
        return []


def parse_attrs(string, attrs):
    sensors = []
    for it in attrs:
        (label, serie_id) = it
        exp = r"{}:.+?([\d\.]+)".format(re.escape(label))
        match = re.search(exp, string)
        value = float(match.group(1))
        sensors.append((serie_id, value))
    return sensors


# Call command
out, err = executor.call('/usr/bin/sensors')

# Parse and save values
points = parse_sensors(DEVICES, out)
repository.save_snapshot(points, test=False)
