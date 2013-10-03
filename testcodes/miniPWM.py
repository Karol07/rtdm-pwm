#! /usr/bin/python
# Enable PWM Timer on Beaglebone
from mmap import mmap
import struct

#L4_WKUP block in L3 memory map 
MMAP_OFFSET = 0x44c00000                # base address of registers
MMAP_SIZE   = 0x48ffffff-MMAP_OFFSET    # size of the register memory space

CM_PER_BASE = 0x44e00000 - MMAP_OFFSET
C_M_BASE = 0x44e10000 - MMAP_OFFSET

DMTIMER1 = 0x44e31000 - MMAP_OFFSET
DMTIMER2 = 0x48040000 - MMAP_OFFSET

DMTIMER1_IRQSTATUS = DMTIMER1 + 0x28
DMTIMER1_IRQENABLE_SET = DMTIMER1 + 0x2c
DMTIMER2_TCRR = DMTIMER2 + 0x3c


CM_PER_EPWMSS1_CLKCTRL = CM_PER_BASE + 0xcc
CM_PER_EPWMSS0_CLKCTRL = CM_PER_BASE + 0xd4
CM_PER_EPWMSS2_CLKCTRL = CM_PER_BASE + 0xd8

C_M_PER_GPMC_AD0 = C_M_BASE+0x800
C_M_PER_GPMC_AD1 = C_M_BASE+0x804
C_M_PER_GPMC_AD2 = C_M_BASE+0x808
C_M_PER_GPMC_AD3 = C_M_BASE+0x80c
C_M_PER_GPMC_AD4 = C_M_BASE+0x810
C_M_PER_GPMC_AD5 = C_M_BASE+0x814
C_M_PER_GPMC_AD6 = C_M_BASE+0x818
C_M_PER_GPMC_AD7 = C_M_BASE+0x81c
C_M_PER_GPMC_AD8 = C_M_BASE+0x820
C_M_PER_GPMC_AD9 = C_M_BASE+0x824
C_M_PER_GPMC_AD10 = C_M_BASE+0x828

C_M_PER_GPMC_A2 = C_M_BASE+0x848

PWMSS_CTRL = C_M_BASE + 0x664

PWMSS1 = 0x48302000 - MMAP_OFFSET
EPWM1 = 0x48302200 - MMAP_OFFSET #ePWM1, PWM Subsystem 1
EPWM2 = 0x48304200 - MMAP_OFFSET #ePWM2, PWM Subsystem 2

PWMSS1_IDVER = PWMSS1 + 0x0
PWMSS1_SYSCONFIG = PWMSS1 + 0x4
PWMSS1_CLKCONFIG = PWMSS1 + 0x8
PWMSS1_CLKSTATUS = PWMSS1 + 0xc

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

#values
#SYSTEM_CLOCK 234E3
#TBCLK 234E3
#PWM_CARRIER 50
#PWM_DUTY_RATIO_A 2e-1
#PWM_DUTY_RATIO_B 1e-1

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

""" Confure ehrpwm counter for up-count mode """
val = _getReg(EPWM1_TBCTL)
print "Register EPWM1_TBCTL was " + hex(val)
_setReg(EPWM1_TBCTL,0x1ca00)
val = _getReg(EPWM1_TBCTL)
print "Register EPWM1_TBCTL changed to " + hex(val)

""" TBPHS """
val = _getReg(EPWM1_TBSTS)
print "Register EPWM1_TBSTS was " + hex(val)
_setReg(EPWM1_TBSTS,0x1)
val = _getReg(EPWM1_TBSTS)
print "Register EPWM1_TBSTS was " + hex(val)

val = _getReg(EPWM1_TBPHSHR)
print "Register EPWM1_TBPHSHR was " + hex(val)
_setReg(EPWM1_TBPHSHR,0x0)
val = _getReg(EPWM1_TBPHSHR)
print "Register EPWM1_TBPHSHR changed to " + hex(val)

val = _getReg(EPWM1_TBPHS)
print "Register EPWM1_TBPHS was " + hex(val)
_setReg(EPWM1_TBPHS,0x99890000L)
val = _getReg(EPWM1_TBPHS)
print "Register EPWM1_TBPHS changed to " + hex(val)

val = _getReg(EPWM1_TBCNT)
print "Register EPWM1_TBCNT was " + hex(val)
_setReg(EPWM1_TBCNT,0xf4249a01L)
val = _getReg(EPWM1_TBCNT)
print "Register EPWM1_TBCNT was " + hex(val)

""" Setup shadowing (pwm_config in tiehrpwm) """
val = _getReg(EPWM1_CMPCTL)
print "Register EPWM1_CMPCTL was " + hex(val)
_setReg(EPWM1_CMPCTL,0x0)
val = _getReg(EPWM1_CMPCTL)
print "Register EPWM1_CMPCTL changed to " + hex(val)




""" Setup Period """
prdval = _getReg(EPWM1_TBPRD)
print "Register EPWM1_TBPRD was " + hex(prdval)
#_setReg(EPWM1_TBPRD,0xf424)
#val = _getReg(EPWM1_TBPRD)
#print "Register EPWM1_TBPRD changed to " + hex(val)

""" set duty cycle with CMP (p2056) """
val = _getReg(EPWM1_CMPA)
print "Register EPWM1_CMPA was " + hex(val)
#_setReg(EPWM1_CMPA,(prdval+1)*2e-1)
val = _getReg(EPWM1_CMPA)
print "Register EPWM1_CMPA changed to " + hex(val)
#
#val = _getReg(EPWM1_CMPB)
#print "Register EPWM1_CMPB was " + hex(val)
#_setReg(EPWM1_CMPB,0x250000)
#val = _getReg(EPWM1_CMPB)
#print "Register EPWM1_CMPB changed to " + hex(val)
#
#

#val = _getReg(EPWM1_CMPAHR)
#print "Register EPWM1_CMPAHR was " + hex(val)
#_setReg(EPWM1_CMPAHR,0x5b8d0000)
#val = _getReg(EPWM1_CMPAHR)
#print "Register EPWM1_CMPAHR was " + hex(val)
#
#

