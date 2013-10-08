#! /usr/bin/python
# Enable PWM Timer on Beaglebone
from mmap import mmap
import struct

#L4_WKUP block in L3 memory map 
MMAP_OFFSET = 0x44c00000                # base address of registers
MMAP_SIZE   = 0x48ffffff-MMAP_OFFSET    # size of the register memory space

CM_PER_BASE = 0x44e00000 - MMAP_OFFSET
CM_PER_EPWMSS1_CLKCTRL = CM_PER_BASE + 0xcc
CM_PER_EPWMSS0_CLKCTRL = CM_PER_BASE + 0xd4
CM_PER_EPWMSS2_CLKCTRL = CM_PER_BASE + 0xd8

EPWM1 = 0x48302200 - MMAP_OFFSET #ePWM1, PWM Subsystem 1
EPWM1_TBCTL = EPWM1 + 0x0 #offset 3Ch (P9_14)
EPWM1_TBSTS = EPWM1 + 0x2
EPWM1_TBPHSHR = EPWM1 + 0x4
EPWM1_TBPHS = EPWM1 + 0x6
EPWM1_TBCNT = EPWM1 + 0x8
EPWM1_TBPRD = EPWM1 + 0xA 
EPWM1_CMPCTL = EPWM1 + 0xE #offset 3Ch (P9_14)
EPWM1_CMPAHR = EPWM1 + 0x10
EPWM1_CMPA = EPWM1 + 0x12 #offset 3Ch (P9_14)
EPWM1_CMPB = EPWM1 + 0x14 #offset 3Ch (P9_14)
EPWM1_AQCTLA = EPWM1 + 0x16 #offset 3Ch (P9_14)
EPWM1_AQCTLB = EPWM1 + 0x18 #offset 3Ch (P9_14)
EPWM1_AQSFRC = EPWM1 + 0x1A
EPWM1_DBCTL = EPWM1 + 0x1E
EPWM1_DBRED = EPWM1 + 0x20
EPWM1_DBFED = EPWM1 + 0x22
EPWM1_TZSEL = EPWM1 + 0x24
EPWM1_TZCTL = EPWM1 + 0x28
EPWM1_TZEINT = EPWM1 + 0x2A
EPWM1_TZFLG = EPWM1 + 0x2C
EPWM1_TZCLR = EPWM1 + 0x2E
EPWM1_TZFRC = EPWM1 + 0x30
EPWM1_ETSEL = EPWM1 + 0x32 #offset 3Ch (P9_14)
EPWM1_ETPS = EPWM1 + 0x34 #offset 3Ch (P9_14)
EPWM1_ETFLG = EPWM1 + 0x36
EPWM1_ETCLR = EPWM1 + 0x38
EPWM1_PCCTL = EPWM1 + 0x3c #offset 3Ch (P9_14)
EPWM1_HRCTL = EPWM1 + 0x40 

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
def _pwm_tbctl(address, mask):
    _andReg(address,0xf8ff)
    _orReg(address,mask << 8)

val = _getReg(CM_PER_EPWMSS1_CLKCTRL)
print "Register CM_PER_EPWMSS1_CLKCTRL was " + hex(val)
_setReg(CM_PER_EPWMSS1_CLKCTRL, 0x2)
val = _getReg(CM_PER_EPWMSS1_CLKCTRL)
print "Register CM_PER_EPWMSS1_CLKCTRL changed to " + hex(val)

val = _getReg(CM_PER_EPWMSS0_CLKCTRL)
print "Register CM_PER_EPWMSS0_CLKCTRL was " + hex(val)
_setReg(CM_PER_EPWMSS0_CLKCTRL, 0x2)
val = _getReg(CM_PER_EPWMSS0_CLKCTRL)
print "Register CM_PER_EPWMSS0_CLKCTRL changed to " + hex(val)


val = _getReg(CM_PER_EPWMSS2_CLKCTRL)
print "Register CM_PER_EPWMSS2_CLKCTRL was " + hex(val)
_setReg(CM_PER_EPWMSS2_CLKCTRL, 0x2)
val = _getReg(CM_PER_EPWMSS2_CLKCTRL)
print "Register CM_PER_EPWMSS2_CLKCTRL changed to " + hex(val)


def register_fix(node, name, value):
	val = _getReg(node)
	print "Register "+name+" was " + hex(val)
	_setReg(node,value)
	val = _getReg(node)
	print "Register "+name+" changed to " + hex(val)


orReg(EPWM1_TBCTL,0x1 << 3)

register_fix(EPWM1_TBPRD,"PRD",0x258)
register_fix(EPWM1_TBPHS,"PHS",0x0)
register_fix(EPWM1_TBCNT,"CNT",0x0)

#EPWM1_TBCTL |= 0x1
#EPWM1_TBCTL |= 0x0 << 2
#EPWM1_TBCTL |= 0x0 << 3
#EPWM1_TBCTL |= 0x3 << 4
#EPWM1_TBCTL |= 0x0 << 8
#EPWM1_TBCTL |= 0x0 << 10
#register_fix(EPWM1_TBCTL,"CTL",0x31)
val = _getReg(EPWM1_TBCTL)
print "Register EPWM1_TBCTL changed to " + hex(val)

register_fix(EPWM1_TBCNT,"CNT",0x0)

register_fix(EPWM1_CMPA,"CMPA",0x15e)
register_fix(EPWM1_CMPB,"CMPB",0xc8)

#EPWM1_CMPCTL |= 0x0
#EPWM1_CMPCTL |= 0x0 << 2
#EPWM1_CMPCTL |= 0x0 << 4
#EPWM1_CMPCTL |= 0x0 << 5
register_fix(EPWM1_CMPCTL,"CMPCTL",0x0)

val = _getReg(EPWM1_AQCTLA)
print "Register EPWM1_AQCTLA was " + hex(val)
val = _getReg(EPWM1_AQCTLB)
print "Register EPWM1_AQCTLB was " + hex(val)


EPWM1_AQCTLA |= 0x2 
EPWM1_AQCTLA |= 0x1 << 4

EPWM1_AQCTLB |= 0x2 
EPWM1_AQCTLB |= 0x1 <<8 
register_fix(EPWM1_CMPCTL,"CMPCTL",0x12)
register_fix(EPWM1_CMPCTL,"CMPCTL",0x102)


