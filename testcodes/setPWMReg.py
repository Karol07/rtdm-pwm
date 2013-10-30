#! /usr/bin/python
# Enable PWM Timer on Beaglebone
from mmap import mmap
import struct
MMAP_OFFSET = 0x44c00000                # base address of registers
MMAP_SIZE   = 0x48ffffff-MMAP_OFFSET    # size of the register memory space
CM_PER_BASE = 0x44e00000 - MMAP_OFFSET
CM_PER_EPWMSS1_CLKCTRL = CM_PER_BASE + 0xcc
CM_PER_EPWMSS0_CLKCTRL = CM_PER_BASE + 0xd4
CM_PER_EPWMSS2_CLKCTRL = CM_PER_BASE + 0xd8

EPWM1 = 0x48302200 - MMAP_OFFSET #ePWM1, PWM Subsystem 1
EPWM2 = 0x48304200 - MMAP_OFFSET #ePWM2, PWM Subsystem 2

EPWM1_TBPRD = EPWM1 + 0xA 
EPWM1_TBCNT = EPWM1 + 0x8
EPWM1_CMPA = EPWM1 + 0x12 #offset 3Ch (P9_14)
EPWM1_CMPB = EPWM1 + 0x14 #offset 3Ch (P9_14)
EPWM1_CMPAHR = EPWM1 + 0x10
EPWM1_TBCTL = EPWM1 + 0x0 #offset 3Ch (P9_14)
EPWM1_TBSTS = EPWM1 + 0x2
EPWM1_TBPHSHR = EPWM1 + 0x4
EPWM1_TBPHS = EPWM1 + 0x6

with open("/dev/mem", "r+b") as f:
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
val = _getReg(CM_PER_EPWMSS1_CLKCTRL)
print "Register CM_PER_EPWMSS1_CLKCTRL was " + hex(val)
_setReg(CM_PER_EPWMSS1_CLKCTRL, 0x2)
val = _getReg(CM_PER_EPWMSS1_CLKCTRL)
print "Register CM_PER_EPWMSS1_CLKCTRL changed to " + hex(val)

def register_fix(node, name, value):
	val = _getReg(node)
	print "Register "+name+" was " + hex(val)
	_setReg(node,value)
	val = _getReg(node)
	print "Register "+name+" changed to " + hex(val)

SYSCLK = 50000000 #18750000
freq = 600
duty = 50

tbprd = SYSCLK/freq
fixed = hex(tbprd<<16).rstrip("L")[:10]
fixed = int(fixed,16)
register_fix(EPWM1_TBCNT,"TBCNT",fixed)
register_fix(EPWM1_TBPHS,"TBPHS",0x0)
register_fix(EPWM1_TBPHSHR,"TBPHSHR",0x0)
#register_fix(EPWM1_TBCNT,"TBCNT",0x3500000)
#register_fix(EPWM1_TBPHSHR,"TBPHSHR",0x61330000)
#register_fix(EPWM1_TBCNT,"TBCNT",0xf42f0000)

print "TBPHS "+ str(_getReg(EPWM1_TBPHS))

#register_fix(EPWM1_TBCTL,"TBCTL",0x5c080)
#register_fix(EPWM1_TBSTS,"TBSTS",0x5)


TBPRD = _getReg(EPWM1_TBPRD)
det = (TBPRD +1) * (duty * 0.01)
det = int(det) << 16
register_fix(EPWM1_CMPAHR,"CMPAHR",int(det))

print "TBPRD "+str(hex(TBPRD))
TBCNT = _getReg(EPWM1_TBCNT)
print "TBCNT "+str(hex(TBCNT))

