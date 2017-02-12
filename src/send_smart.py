import re
import command_executor as executor
from repository import save_snapshot

DEVICES = ['sda', 'sdb', 'sdc']


def parse_smart(device, string):
    # Get model and serial
    model = re.search(r"Device Model: +(.+)", string).group(1)
    serial = re.search(r"Serial Number: +(.+)", string).group(1)

    # Get attributes
    attrs = []
    attr_lines = re.finditer(r"[^\r\n\d]*(\d+ +[\w_-]+ +0x\d+[^\r\n]*)", string)
    attr_lines = [it.group(1) for it in attr_lines]
    attr_splits = [re.split(r" +", it) for it in attr_lines]
    for split in attr_splits:
        attr_id = split[0]
        attr_name = re.sub(r"[^\w\d_]", '', split[1])
        serie_id = 'drive.{}.{}_{}'.format(device, attr_id, attr_name)
        raw_val = int(re.match(r"(\d+)", split[9]).group(1))
        attrs.append((serie_id, raw_val))

    return attrs


# Get S.M.A.R.T. for each device
for dev in DEVICES:
    # Call command
    cmd = '/usr/sbin/smartctl -a -d ata /dev/{}'.format(dev)
    out, err = executor.call(cmd)

    # Parse and save values
    points = parse_smart(dev, out)
    save_snapshot(points, test=False)
