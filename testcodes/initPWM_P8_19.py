#! /usr/bin/python
# Enable PWM Timer on Beaglebone
from mmap import mmap
import struct

#L4_WKUP block in L3 memory map 
MMAP_OFFSET = 0x44c00000                # base address of registers
MMAP_SIZE   = 0x48ffffff-MMAP_OFFSET    # size of the register memory space

CM_PER_BASE = 0x44e00000 - MMAP_OFFSET
C_M_BASE = 0x44e10000 - MMAP_OFFSET

CM_PER_EPWMSS1_CLKCTRL = CM_PER_BASE + 0xcc
CM_PER_EPWMSS0_CLKCTRL = CM_PER_BASE + 0xd4
CM_PER_EPWMSS2_CLKCTRL = CM_PER_BASE + 0xd8

PWMSS_CTRL = C_M_BASE + 0x664

PWMSS1 = 0x48302000 - MMAP_OFFSET
EPWM1 = 0x48302200 - MMAP_OFFSET #ePWM1, PWM Subsystem 1
EPWM2 = 0x48304200 - MMAP_OFFSET #ePWM2, PWM Subsystem 2

PWMSS1_IDVER = PWMSS1 + 0x0
PWMSS1_SYSCONFIG = PWMSS1 + 0x4
PWMSS1_CLKCONFIG = PWMSS1 + 0x8
PWMSS1_CLKSTATUS = PWMSS1 + 0xc

EPWM2_TBCTL = EPWM2 + 0x0 #offset 3Ch (P9_14)
EPWM2_TBSTS = EPWM2 + 0x2
EPWM2_TBPHSHR = EPWM2 + 0x4
EPWM2_TBPHS = EPWM2 + 0x6
EPWM2_TBCNT = EPWM2 + 0x8
EPWM2_TBPRD = EPWM2 + 0xA 
EPWM2_CMPCTL = EPWM2 + 0xE #offset 3Ch (P9_14)
EPWM2_CMPAHR = EPWM2 + 0x10
EPWM2_CMPA = EPWM2 + 0x12 #offset 3Ch (P9_14)
EPWM2_CMPB = EPWM2 + 0x14 #offset 3Ch (P9_14)
EPWM2_AQCTLA = EPWM2 + 0x16 #offset 3Ch (P9_14)
EPWM2_AQCTLB = EPWM2 + 0x18 #offset 3Ch (P9_14)
EPWM2_AQSFRC = EPWM2 + 0x1A
EPWM2_DBCTL = EPWM2 + 0x1E
EPWM2_DBRED = EPWM2 + 0x20
EPWM2_DBFED = EPWM2 + 0x22
EPWM2_TZSEL = EPWM2 + 0x24
EPWM2_TZCTL = EPWM2 + 0x28
EPWM2_TZEINT = EPWM2 + 0x2A
EPWM2_TZFLG = EPWM2 + 0x2C
EPWM2_TZCLR = EPWM2 + 0x2E
EPWM2_TZFRC = EPWM2 + 0x30
EPWM2_ETSEL = EPWM2 + 0x32 #offset 3Ch (P9_14)
EPWM2_ETPS = EPWM2 + 0x34 #offset 3Ch (P9_14)
EPWM2_ETFLG = EPWM2 + 0x36
EPWM2_ETCLR = EPWM2 + 0x38
EPWM2_PCCTL = EPWM2 + 0x3c #offset 3Ch (P9_14)
EPWM2_HRCTL = EPWM2 + 0x40 

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


_setReg(PWMSS1_IDVER, 0x47400001)
_setReg(PWMSS1_SYSCONFIG, 0xcc)
_setReg(PWMSS1_CLKCONFIG, 0x111)
_setReg(PWMSS1_CLKSTATUS, 0x111)

val = _getReg(PWMSS1_IDVER)
print "Register PWMSS1_IDVER was " + hex(val)
val = _getReg(PWMSS1_SYSCONFIG)
print "Register PWMSS1_SYSCONFIG was " + hex(val)
val = _getReg(PWMSS1_CLKCONFIG)
print "Register PWMSS1_CLKCONFIG was " + hex(val)
val = _getReg(PWMSS1_CLKSTATUS)
print "Register PWMSS1_CLKSTATUS was " + hex(val)


""" Setup contermode and clock"""
val = _getReg(PWMSS_CTRL)
print "Register PWMSS_CTRL was " + hex(val)
_setReg(PWMSS_CTRL, 0x0)
val = _getReg(PWMSS_CTRL)
print "Register PWMSS_CTRL changed to " + hex(val)
#pwmss_ctrl PWMSS2_TBCLKEN = 1
#pwmss_ctrl PWMSS1_TBCLKEN = 1
#pwmss_ctrl PWMSS0_TBCLKEN = 1

""" Confure ehrpwm counter for up-count mode """
val = _getReg(EPWM2_TBCTL)
print "Register EPWM2_TBCTL was " + hex(val)
_setReg(EPWM2_TBCTL,0x1ca00)
val = _getReg(EPWM2_TBCTL)
print "Register EPWM2_TBCTL changed to " + hex(val)
#val = _getReg(EPWM2_TBCTL)
#print "Register EPWM2_TBCTL changed to " + hex(val)
#TBCTL CTRMODE = 0 #up-count mode
#TBCTL HSPCLKDIV 5
#TBCTL CLKDIV 6
#TBCTL PRDLD = 0

""" TBPHS """
val = _getReg(EPWM2_TBSTS)
print "Register EPWM2_TBSTS was " + hex(val)
_setReg(EPWM2_TBSTS,0x1)
val = _getReg(EPWM2_TBSTS)
print "Register EPWM2_TBSTS was " + hex(val)

val = _getReg(EPWM2_TBPHSHR)
print "Register EPWM2_TBPHSHR was " + hex(val)
_setReg(EPWM2_TBPHSHR,0x0)
val = _getReg(EPWM2_TBPHSHR)
print "Register EPWM2_TBPHSHR changed to " + hex(val)

val = _getReg(EPWM2_TBPHS)
print "Register EPWM2_TBPHS was " + hex(val)
_setReg(EPWM2_TBPHS,0x99890000L)
val = _getReg(EPWM2_TBPHS)
print "Register EPWM2_TBPHS changed to " + hex(val)

val = _getReg(EPWM2_TBCNT)
print "Register EPWM2_TBCNT was " + hex(val)
_setReg(EPWM2_TBCNT,0xf4249a01L)
val = _getReg(EPWM2_TBCNT)
print "Register EPWM2_TBCNT was " + hex(val)

""" Setup Period """
val = _getReg(EPWM2_TBPRD)
print "Register EPWM2_TBPRD was " + hex(val)
_setReg(EPWM2_TBPRD,0xf424)
val = _getReg(EPWM2_TBPRD)
print "Register EPWM2_TBPRD changed to " + hex(val)

""" Setup shadowing (pwm_config in tiehrpwm) """
val = _getReg(EPWM2_CMPCTL)
print "Register EPWM2_CMPCTL was " + hex(val)
_setReg(EPWM2_CMPCTL,0x0)
val = _getReg(EPWM2_CMPCTL)
print "Register EPWM2_CMPCTL changed to " + hex(val)
#_setReg(EPWM2_CMPCTL,0x0)
#CMPCTL SHDWAMODE = 0
#CMPCTL SHDWBMODE = 0
#CMPCTL LOADAMODE = 0
#CMPCTL LOADBMODE = 0

val = _getReg(EPWM2_CMPAHR)
print "Register EPWM2_CMPAHR was " + hex(val)
_setReg(EPWM2_CMPAHR,0x5b8d0000)
val = _getReg(EPWM2_CMPAHR)
print "Register EPWM2_CMPAHR was " + hex(val)

""" set duty cycle with CMP (p2056) """
val = _getReg(EPWM2_CMPA)
print "Register EPWM2_CMPA was " + hex(val)
_setReg(EPWM2_CMPA,0x5b8d)
val = _getReg(EPWM2_CMPA)
print "Register EPWM2_CMPA changed to " + hex(val)

val = _getReg(EPWM2_CMPB)
print "Register EPWM2_CMPB was " + hex(val)
_setReg(EPWM2_CMPB,0x250000)
val = _getReg(EPWM2_CMPB)
print "Register EPWM2_CMPB changed to " + hex(val)
#_setReg(EPWM2_CMPA,0x0)
#_setReg(EPWM2_CMPB,0x0)
#CMPA duty cycle
#CMPB duty cycle

""" Set actions - AQ (p2096 / configure_polarity in tiehrpwm)"""
val = _getReg(EPWM2_AQCTLA)
print "Register EPWM2_AQCTLA was " + hex(val)
_setReg(EPWM2_AQCTLA,0x25)
val = _getReg(EPWM2_AQCTLA)
print "Register EPWM2_AQCTLA changed to " + hex(val)

val = _getReg(EPWM2_AQCTLB)
print "Register EPWM2_AQCTLB was " + hex(val)
_setReg(EPWM2_AQCTLB,0x0)
val = _getReg(EPWM2_AQCTLB)
print "Register EPWM2_AQCTLB changed to " + hex(val)
#_setReg(EPWM2_AQCTLA,0x1a)
#_setReg(EPWM2_AQCTLB,0x1a)
#AQCTLA ZRO = 2
#AQCTLA CAU = 1 #Up-count
#AQCTLB ZRO = 2
#AQCTLB CBU = 1 #Up-count

val = _getReg(EPWM2_AQSFRC)
print "Register EPWM2_AQSFRC changed to " + hex(val)
val = _getReg(EPWM2_DBCTL)
print "Register EPWM2_DBCTL changed to " + hex(val)
val = _getReg(EPWM2_DBRED)
print "Register EPWM2_DBRED changed to " + hex(val)
val = _getReg(EPWM2_DBFED)
print "Register EPWM2_DBFED changed to " + hex(val)
val = _getReg(EPWM2_TZCTL)
print "Register EPWM2_TZCTL changed to " + hex(val)
val = _getReg(EPWM2_TZEINT)
print "Register EPWM2_TZEINT changed to " + hex(val)
val = _getReg(EPWM2_TZFLG)
print "Register EPWM2_TZFLG changed to " + hex(val)
val = _getReg(EPWM2_TZCLR)
print "Register EPWM2_TZCLR changed to " + hex(val)
val = _getReg(EPWM2_TZFRC)
print "Register EPWM2_TZFRC changed to " + hex(val)

""" Set interrupts ()"""
val = _getReg(EPWM2_ETSEL)
print "Register EPWM2_ETSEL was " + hex(val)
_setReg(EPWM2_ETSEL,0x0)
val = _getReg(EPWM2_ETSEL)
print "Register EPWM2_ETSEL changed to " + hex(val)

val = _getReg(EPWM2_ETPS)
print "Register EPWM2_ETPS was " + hex(val)
_setReg(EPWM2_ETPS,0x0)
val = _getReg(EPWM2_ETPS)
print "Register EPWM2_ETPS changed to " + hex(val)

#_setReg(EPWM2_ETSEL,0x9)
#_setReg(EPWM2_ETPS,0x1)
#ETSEL INSEL = 1
#ETSEL INTEN = 1
#ETPS INTPRD = 1

val = _getReg(EPWM2_ETFLG)
print "Register EPWM2_ETFLG changed to " + hex(val)
val = _getReg(EPWM2_ETCLR)
print "Register EPWM2_ETCLR changed to " + hex(val)
val = _getReg(EPWM2_PCCTL)
print "Register EPWM2_PCCTL changed to " + hex(val)
val = _getReg(EPWM2_HRCTL)
print "Register EPWM2_HRCTL changed to " + hex(val)





""" Setup contermode and clock"""
val = _getReg(PWMSS_CTRL)
print "Register PWMSS_CTRL was " + hex(val)
_setReg(PWMSS_CTRL, 0x7)
val = _getReg(PWMSS_CTRL)
print "Register PWMSS_CTRL changed to " + hex(val)
#pwmss_ctrl PWMSS2_TBCLKEN = 1
#pwmss_ctrl PWMSS1_TBCLKEN = 1
#pwmss_ctrl PWMSS0_TBCLKEN = 1


