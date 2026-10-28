#!/usr/bin/env python3
"""coresnap - copy a process's writable memory to a file.

A minimal, dependency-free "core-style" snapshot used by the fixture-based
regression suite: capture a worker's writable mappings, then replay analysis
offline without keeping the worker alive.

Usage: python3 tools/coresnap.py PID OUT.bin
"""
import re
import sys


def main():
    if len(sys.argv) != 3:
        print("usage: coresnap.py PID OUT.bin")
        return 2
    pid = int(sys.argv[1])
    out_path = sys.argv[2]
    total = 0
    regions = 0
    with open(out_path, "wb") as out:
        with open("/proc/%d/mem" % pid, "rb") as mem:
            for line in open("/proc/%d/maps" % pid):
                m = re.match(r"^([0-9a-f]+)-([0-9a-f]+) rw", line)
                if not m:
                    continue
                s, e = int(m.group(1), 16), int(m.group(2), 16)
                if e - s > 67108864:
                    continue
                try:
                    mem.seek(s)
                    data = mem.read(e - s)
                except OSError:
                    continue
                out.write(b"@@%016x\n" % s)
                out.write(data)
                total += len(data)
                regions += 1
    print("coresnap: wrote %d bytes from %d rw regions of pid %d to %s" % (total, regions, pid, out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
