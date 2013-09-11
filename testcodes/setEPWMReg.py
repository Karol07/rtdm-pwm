#! /usr/bin/python
from mmap import mmap
import struct

MMAP_OFFSET = 0x44c00000                # base address of registers
MMAP_SIZE   = 0x48ffffff-MMAP_OFFSET    # size of the register memory space

P9 = 0x48302200 - MMAP_OFFSET
P9_PCCTL = P9 + 0x3c #offset 3Ch

with open("/dev/mem", "r+b") as f:
    print "memset"
    mem = mmap(f.fileno(), MMAP_SIZE, offset=MMAP_OFFSET)
def _andReg(address, mask):
    """ Sets 32-bit Register at address to its current value AND mask. """
    _setReg(address, _getReg(address)&mask)
def _orReg(address, mask):
    """ Sets 32-bit Register at address to its current value OR mask. """
    _setReg(address, _getReg(address)|mask)
def _xorReg(address, mask):
    """ Sets 32-bit Register at address to its current value XOR mask. """
    _setReg(address, _getReg(address)^mask)
def _getReg(address):
    """ Returns unpacked 32 bit register value starting from address. """
    return struct.unpack("<L", mem[address:address+4])[0]
def _setReg(address, new_value):
    """ Sets 32 bits at given address to given value. """
    mem[address:address+4] = struct.pack("<L", new_value)

val = _getReg(P9_PCCTL)
print "Register P9_PCCTL was " + hex(val)

_orReg(P9_PCCTL,0x1001)

val = _getReg(P9_PCCTL)
print "Register P9_PCCTL was " + hex(val)


