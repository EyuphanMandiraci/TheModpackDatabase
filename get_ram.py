from psutil import virtual_memory


def get_ram():
    max_ram = virtual_memory().total
    max_ram //= 1024
    max_ram //= 1024
    max_ram //= 1024
    return max_ram
