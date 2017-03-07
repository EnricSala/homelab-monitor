import re
import command_executor as executor
import influxdb_repository as repository

INCLUDE_VALUES = False
INCLUDE_PCT = True


def parse_memory(string):
    memory_ids = ['total', 'used', 'free', 'shared', 'cache', 'available']

    # Get RAM use
    ram_string = re.search(r"Mem: +?(\d.*)", string).group(1)
    ram_parts = re.split(r" +", ram_string)
    ram_values = [int(it) for it in ram_parts]
    ram_names = ['memory.ram.' + it for it in memory_ids]
    ram = zip(ram_names, ram_values)

    # Calc RAM percentage
    ram_total = float(ram_values[0])
    ram_pct_values = [round(it / ram_total * 100, 2) for it in ram_values[1:]]
    ram_pct_names = [it + '_pct' for it in ram_names[1:]]
    ram_pct = zip(ram_pct_names, ram_pct_values)

    # Get SWAP use
    swap_string = re.search(r"Swap: +?(\d.*)", string).group(1)
    swap_parts = re.split(r" +", swap_string)
    swap_values = [int(it) for it in swap_parts]
    swap_names = ['memory.swap.' + it for it in memory_ids]
    swap = zip(swap_names, swap_values)

    # Calc SWAP percentage
    swap_total = float(swap_values[0])
    swap_pct_values = [round(it / swap_total * 100, 2) for it in swap_values[1:]]
    swap_pct_names = [it + '_pct' for it in swap_names[1:]]
    swap_pct = zip(swap_pct_names, swap_pct_values)

    # Build result
    result = []
    if INCLUDE_VALUES:
        result = result + ram + swap
    if INCLUDE_PCT:
        result = result + ram_pct + swap_pct
    return result


# Call command
out, err = executor.call('/usr/bin/free -m')

# Parse and save values
points = parse_memory(out)
repository.save_snapshot(points, test=False)
