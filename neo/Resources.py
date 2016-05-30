from mmap import mmap
from os import devnull
from subprocess import call, STDOUT, Popen, PIPE


class ResourceError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class MemoryMap:
    def __init__(self, file_lock):
        self.raw = open(file_lock, "r+b")
        try:
            self.mmap = mmap(self.raw.fileno(), 0)  # Open file in memory
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
        self.mmap[0] = str(digit)
        self.mmap.flush()

    def write_line(self, line):
        self.mmap.seek(0)
        self.mmap.write(line)
        self.mmap.flush()

    def resize(self, size):
        self.mmap.seek(0)
        self.mmap.resize(size)

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
