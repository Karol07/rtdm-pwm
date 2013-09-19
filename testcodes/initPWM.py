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
EPWM1_TBPRD = EPWM1 + 0xA 
EPWM1_CMPCTL = EPWM1 + 0xE #offset 3Ch (P9_14)
EPWM1_CPMA = EPWM1 + 0x12 #offset 3Ch (P9_14)
EPWM1_CPMB = EPWM1 + 0x14 #offset 3Ch (P9_14)
EPWM1_AQCTLA = EPWM1 + 0x16 #offset 3Ch (P9_14)
EPWM1_AQCTLB = EPWM1 + 0x18 #offset 3Ch (P9_14)
EPWM1_ETSEL = EPWM1 + 0x32 #offset 3Ch (P9_14)
EPWM1_PCCTL = EPWM1 + 0x3c #offset 3Ch (P9_14)

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
SYSTEM_CLOCK 234E3
TBCLK 234E3
PWM_CARRIER 50
PWM_DUTY_RATIO_A 2e-1
PWM_DUTY_RATIO_B 1e-1

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

""" Setup contermode and clock"""
val = _getReg(PWMSS_CTRTL)
print "Register PWMSS_CTRTL was " + hex(val)
_setReg(PWMSS_CTRTL, 0x7)
val = _getReg(PWMSS_CTRTL)
print "Register PWMSS_CTRTL changed to " + hex(val)
#pwmss_ctrl PWMSS2_TBCLKEN = 1
#pwmss_ctrl PWMSS1_TBCLKEN = 1
#pwmss_ctrl PWMSS0_TBCLKEN = 1

""" Confure ehrpwm counter for up-count mode """
_setReg(EPWM1_TBCTL,0xd40)
_setReg(EPWM2_TBCTL,0xd40)
#TBCTL CTRMODE = 0 #up-count mode
#TBCTL HSPCLKDIV 5
#TBCTL CLKDIV 6
#TBCTL PRDLD = 0

""" Setup Period """
_setReg(EPWM1_TBPRD,0x33)

""" Setup shadowing (pwm_config in tiehrpwm) """
_setReg(EPWM1_CMPCTL,0x0)
_setReg(EPWM2_CMPCTL,0x0)
#CMPCTL SHDWAMODE = 0
#CMPCTL SHDWBMODE = 0
#CMPCTL LOADAMODE = 0
#CMPCTL LOADBMODE = 0

""" set duty cycle with CMP (p2056) """
_setReg(EPWM1_CMPA,0x0)
_setReg(EPWM1_CMPB,0x0)
_setReg(EPWM2_CMPA,0x0)
_setReg(EPWM2_CMPB,0x0)
#CMPA duty cycle
#CMPB duty cycle

""" Set actions - AQ (p2096 / configure_polarity in tiehrpwm)"""
_setReg(EPWM1_AQCTLA,0x1a)
_setReg(EPWM1_AQCTLB,0x1a)
_setReg(EPWM2_AQCTLA,0x1a)
_setReg(EPWM2_AQCTLB,0x1a)
#AQCTLA ZRO = 2
#AQCTLA CAU = 1 #Up-count
#AQCTLB ZRO = 2
#AQCTLB CBU = 1 #Up-count

""" Set interrupts ()"""
_setReg(EPWM1_ETSEL,0x9)
_setReg(EPWM2_ETSEL,0x9)
_setReg(EPWM1_ETPS,0x1)
_setReg(EPWM2_ETPS,0x1)
#ETSEL INSEL = 1
#ETSEL INTEN = 1
#ETPS INTPRD = 1
