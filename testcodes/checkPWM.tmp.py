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
PWMSS_CTRL = CM_PER_BASE + 0x664

EPWM1 = 0x48302200 - MMAP_OFFSET #ePWM1, PWM Subsystem 1
EPWM2 = 0x48304200 - MMAP_OFFSET #ePWM2, PWM Subsystem 2

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

EPWM2_TBCTL = EPWM2 + 0x0 #offset 3Ch (P8_19)
EPWM2_TBPRD = EPWM2 + 0xA 
EPWM2_PCCTL = EPWM2 + 0x3c #offset 3Ch (P8_19)
EPWM2_CMPCTL = EPWM2 + 0xE #offset 3Ch (P8_19)
EPWM2_CMPA = EPWM2 + 0x12 #offset 3Ch (P8_19)
EPWM2_CMPB = EPWM2 + 0x14 #offset 3Ch (P8_19)
EPWM2_AQCTLA = EPWM2 + 0x16 #offset 3Ch (P8_19)
EPWM2_AQCTLB = EPWM2 + 0x18 #offset 3Ch (P8_19)
EPWM2_ETSEL = EPWM2 + 0x32 #offset 3Ch (P8_19)
EPWM2_ETPS = EPWM2 + 0x34 #offset 3Ch (P8_19)
EPWM2_PCCTL = EPWM2 + 0x3c #offset 3Ch (P8_19)

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

""" Setup contermode and clock"""
val = _getReg(PWMSS_CTRL)
print "Register PWMSS_CTRL was " + hex(val)

""" Confure ehrpwm counter for up-count mode """
val = _getReg(EPWM1_TBCTL)
print "Register EPWM1_TBCTL was " + hex(val)

""" TBPHS """
val = _getReg(EPWM1_TBSTS)
print "Register EPWM1_TBSTS was " + hex(val)
val = _getReg(EPWM1_TBPHSHR)
print "Register EPWM1_TBPHSHR was " + hex(val)
val = _getReg(EPWM1_TBPHS)
print "Register EPWM1_TBPHS was " + hex(val)
val = _getReg(EPWM1_TBCNT)
print "Register EPWM1_TBCNT was " + hex(val)

""" Setup Period """
val = _getReg(EPWM1_TBPRD)
print "Register EPWM1_TBPRD was " + hex(val)

""" Setup shadowing (pwm_config in tiehrpwm) """
val = _getReg(EPWM1_CMPCTL)
print "Register EPWM1_CMPCTL was " + hex(val)

val = _getReg(EPWM1_CMPAHR)
print "Register EPWM1_CMPAHR was " + hex(val)

""" set duty cycle with CMP (p2056) """
val = _getReg(EPWM1_CMPA)
print "Register EPWM1_CMPA was " + hex(val)
val = _getReg(EPWM1_CMPB)
print "Register EPWM1_CMPB was " + hex(val)

""" Set actions - AQ (p2096 / configure_polarity in tiehrpwm)"""
val = _getReg(EPWM1_AQCTLA)
print "Register EPWM1_AQCTLA was " + hex(val)
val = _getReg(EPWM1_AQCTLB)
print "Register EPWM1_AQCTLB was " + hex(val)

val = _getReg(EPWM1_AQSFRC)
print "Register EPWM1_AQSFRC was " + hex(val)
val = _getReg(EPWM1_DBCTL)
print "Register EPWM1_DBCTL was " + hex(val)
val = _getReg(EPWM1_DBRED)
print "Register EPWM1_DBRED was " + hex(val)
val = _getReg(EPWM1_DBFED)
print "Register EPWM1_DBFED was " + hex(val)
val = _getReg(EPWM1_TZCTL)
print "Register EPWM1_TZCTL was " + hex(val)
val = _getReg(EPWM1_TZEINT)
print "Register EPWM1_TZEINT was " + hex(val)
val = _getReg(EPWM1_TZFLG)
print "Register EPWM1_TZFLG was " + hex(val)
val = _getReg(EPWM1_TZCLR)
print "Register EPWM1_TZCLR was " + hex(val)
val = _getReg(EPWM1_TZFRC)
print "Register EPWM1_TZFRC was " + hex(val)

""" Set interrupts ()"""
val = _getReg(EPWM1_ETSEL)
print "Register EPWM1_ETSEL was " + hex(val)
val = _getReg(EPWM1_ETPS)
print "Register EPWM1_ETPS was " + hex(val)

val = _getReg(EPWM1_ETFLG)
print "Register EPWM1_ETFLG was " + hex(val)
val = _getReg(EPWM1_ETCLR)
print "Register EPWM1_ETCLR was " + hex(val)
val = _getReg(EPWM1_PCCTL)
print "Register EPWM1_PCCTL was " + hex(val)
val = _getReg(EPWM1_HRCTL)
print "Register EPWM1_HRCTL was " + hex(val)


