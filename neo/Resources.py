# from mmap import mmap, PAGESIZE, MAP_SHARED, PROT_WRITE, PROT_READ
from subprocess import Popen, PIPE


class ResourceError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class MemoryMap:
    def __init__(self, file_lock, mode="r+b"):
        self.raw = open(file_lock, mode)  # O_RDWR | O_SYNC)
        try:
            self.mmap = self.raw
            # @TODO work on actually getting this to work
            # self.mmap = mmap(self.raw.fileno(), PAGESIZE, MAP_SHARED, PROT_WRITE)  # Open file in memory
        except ValueError:
            raise ResourceError("Couldn't lock file into memory: %s" % file_lock)

    @staticmethod
    def only_digit(string):
        try:
            return int(string)
        except ValueError:
            return 0

    def read_digit(self):
        self.raw.seek(0)
        self.raw.flush()
        return self.only_digit(self.raw.read(1))

    def read_line(self):
        self.raw.seek(0)
        return self.raw.readline()

    def write_digit(self, digit):
        self.mmap.seek(0)
        self.mmap.write(str(digit))
        # self.mmap[0] = str(digit)
        self.mmap.flush()

    def write_line(self, line):
        self.mmap.seek(0)
        self.mmap.write(line)
        self.mmap.flush()

    '''
    def resize(self, size):
        self.mmap.seek(0)
        self.mmap.resize(size)
    '''

    def close(self):
        try:
            self.mmap.close()
            self.raw.close()
        except (OSError, IOError, TypeError):
            pass


class Command:
    def __init__(self):
        self.prints = False

    def run(self, comms):
        child = Popen(comms, stderr=PIPE, stdout=PIPE, shell=True)
        out, error = child.communicate()
        toret = out + ("" if error is None else error)
        code = child.returncode
        if self.prints:
            print toret
        return [code, toret]


# @TODO WORK ON MEMORY MAPPING
# @TODO CREATE STATIC METHOD CALLING FOR EASYGPIO (NO RESOURCE RELOADING)

''' TEST GPIO 24 PXCLK (FAIL)
start = 0x0209C000
end = 0x0209FFFF
size = end - start
print size

oe = 0x134
usr1 = 1 << 24

out = 0x194
clear = 0x190

from time import sleep

with open("/dev/mem", "r+b") as f:
    mem = mmap(f.fileno(), size, MAP_SHARED, PROT_WRITE | PROT_READ, offset=start)
print mem
exit(1)
packed = mem[oe + oe + 4]

reg_status = struct.unpack("<L", packed)[0]
reg_status &= ~(usr1)
mem[oe + oe + 4] = struct.unpack("<L", packed)[0]

while True:
    try:
        mem[out + out + 4] = struct.unpack("<L", packed)[0]
        sleep(1)
        mem[clear + clear + 4] = struct.unpack("<L", packed)[0]
        sleep(1)
    except:
        break

mem.close()
'''
