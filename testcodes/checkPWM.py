#! /usr/bin/python
# Enable PWM Timer on Beaglebone
from mmap import mmap
import struct

#L4_WKUP block in L3 memory map 
MMAP_OFFSET = 0x44c00000                # base address of registers
MMAP_SIZE   = 0x48ffffff-MMAP_OFFSET    # size of the register memory space

CM_PER_BASE = 0x44e00000 - MMAP_OFFSET
C_M_BASE = 0x44e10000 - MMAP_OFFSET
DMTIMER0 = 0x44e05000 - MMAP_OFFSET
DMTIMER1 = 0x44e31000 - MMAP_OFFSET
DMTIMER2 = 0x48040000 - MMAP_OFFSET
DMTIMER3 = 0x48042000 - MMAP_OFFSET
DMTIMER4 = 0x48044000 - MMAP_OFFSET
DMTIMER5 = 0x48046000 - MMAP_OFFSET
DMTIMER6 = 0x48048000 - MMAP_OFFSET
DMTIMER7 = 0x4804a000 - MMAP_OFFSET

timers = []
timers.append(DMTIMER0)
timers.append(DMTIMER1)
timers.append(DMTIMER2)
timers.append(DMTIMER3)
timers.append(DMTIMER4)
timers.append(DMTIMER5)
timers.append(DMTIMER6)
timers.append(DMTIMER7)

CM_PER_EPWMSS1_CLKCTRL = CM_PER_BASE + 0xcc
CM_PER_EPWMSS0_CLKCTRL = CM_PER_BASE + 0xd4
CM_PER_EPWMSS2_CLKCTRL = CM_PER_BASE + 0xd8

C_M_PER_REVISION = C_M_BASE+0x0
C_M_PER_HWINFO = C_M_BASE+0x4
C_M_PER_SYSCONFIG = C_M_BASE+0x10
C_M_PER_STATUS = C_M_BASE+0x40


PWMSS_CTRL = C_M_BASE + 0x664
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

PWMSS1 = 0x48302000 - MMAP_OFFSET
ECAP1 = 0x48302100 - MMAP_OFFSET
EQEP1 = 0x48302180 - MMAP_OFFSET

EPWM1 = 0x48302200 - MMAP_OFFSET #ePWM1, PWM Subsystem 1
EPWM2 = 0x48304200 - MMAP_OFFSET #ePWM2, PWM Subsystem 2

PWMSS1_IDVER = PWMSS1 + 0x0
PWMSS1_SYSCONFIG = PWMSS1 + 0x4
PWMSS1_CLKCONFIG = PWMSS1 + 0x8
PWMSS1_CLKSTATUS = PWMSS1 + 0xc

ECAP1_TSCTR = ECAP1 + 0x0
ECAP1_CTRPHS = ECAP1 + 0x4
ECAP1_CAP1 = ECAP1 + 0x8
ECAP1_CAP2 = ECAP1 + 0xc
ECAP1_CAP3 = ECAP1 + 0x10
ECAP1_CAP4 = ECAP1 + 0x14
ECAP1_ECCTL1 = ECAP1 + 0x28
ECAP1_ECCTL2 = ECAP1 + 0x2a
ECAP1_ECEINT = ECAP1 + 0x2c
ECAP1_ECFLG = ECAP1 + 0x2e
ECAP1_ECCLR = ECAP1 + 0x30
ECAP1_ECFRC = ECAP1 + 0x32
ECAP1_REVID = ECAP1 + 0x5c

EQEP1_QPOSCNT =EQEP1+0x0
EQEP1_QPOSINIT=EQEP1+0x4
EQEP1_QPOSMAX=EQEP1+0x8
EQEP1_QPOSCMP=EQEP1+0xc
EQEP1_QPOSILAT=EQEP1+0x10
EQEP1_QPOSSLAT=EQEP1+0x14
EQEP1_QPOSLAT=EQEP1+0x18
EQEP1_QUTMR=EQEP1+0x1c
EQEP1_QUPRD=EQEP1+0x20
EQEP1_QWDTMR=EQEP1+0x24
EQEP1_QWDPRD=EQEP1+0x26
EQEP1_QDECCTL=EQEP1+0x28
EQEP1_QEPCTL=EQEP1+0x2a
EQEP1_QCAPCTL=EQEP1+0x2c
EQEP1_QPOSCTL=EQEP1+0x2e
EQEP1_QEINT=EQEP1+0x30
EQEP1_QFLG=EQEP1+0x32
EQEP1_QCLR=EQEP1+0x34
EQEP1_QFRC=EQEP1+0x36
EQEP1_QEPSTS=EQEP1+0x38
EQEP1_QCTMR=EQEP1+0x3a
EQEP1_QCPRD=EQEP1+0x3c
EQEP1_QCTMRLAT=EQEP1+0x3e
EQEP1_QCPRDLAT=EQEP1+0x40
EQEP1_REVID=EQEP1+0x5c

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
val = _getReg(CM_PER_EPWMSS0_CLKCTRL)
print "Register CM_PER_EPWMSS0_CLKCTRL was " + hex(val)
val = _getReg(CM_PER_EPWMSS2_CLKCTRL)
print "Register CM_PER_EPWMSS2_CLKCTRL was " + hex(val)

print "Register C_M_PER_REVISION was " + hex(_getReg(C_M_PER_REVISION))
print "Register C_M_PER_HWINFO was " + hex(_getReg(C_M_PER_HWINFO))
print "Register C_M_PER_SYSCONFIG was " + hex(_getReg(C_M_PER_SYSCONFIG))
print "Register C_M_PER_STATUS was " + hex(_getReg(C_M_PER_STATUS))

print "Register C_M_PER_GPMC_AD0 was " + hex(_getReg(C_M_PER_GPMC_AD0))
print "Register C_M_PER_GPMC_AD1 was " + hex(_getReg(C_M_PER_GPMC_AD1))
print "Register C_M_PER_GPMC_AD2 was " + hex(_getReg(C_M_PER_GPMC_AD2))
print "Register C_M_PER_GPMC_AD3 was " + hex(_getReg(C_M_PER_GPMC_AD3))
print "Register C_M_PER_GPMC_AD4 was " + hex(_getReg(C_M_PER_GPMC_AD4))
print "Register C_M_PER_GPMC_AD5 was " + hex(_getReg(C_M_PER_GPMC_AD5))
print "Register C_M_PER_GPMC_AD6 was " + hex(_getReg(C_M_PER_GPMC_AD6))
print "Register C_M_PER_GPMC_AD7 was " + hex(_getReg(C_M_PER_GPMC_AD7))
print "Register C_M_PER_GPMC_AD8 was " + hex(_getReg(C_M_PER_GPMC_AD8))
print "Register C_M_PER_GPMC_AD9 was " + hex(_getReg(C_M_PER_GPMC_AD9))
print "Register C_M_PER_GPMC_AD10 was " + hex(_getReg(C_M_PER_GPMC_AD10))
print "Register C_M_PER_GPMC_A2 was " + hex(_getReg(C_M_PER_GPMC_A2))

val = _getReg(PWMSS1_IDVER)
print "Register PWMSS1_IDVER was " + hex(val)
val = _getReg(PWMSS1_SYSCONFIG)
print "Register PWMSS1_SYSCONFIG was " + hex(val)
val = _getReg(PWMSS1_CLKCONFIG)
print "Register PWMSS1_CLKCONFIG was " + hex(val)
val = _getReg(PWMSS1_CLKSTATUS)
print "Register PWMSS1_CLKSTATUS was " + hex(val)

val = _getReg(ECAP1_TSCTR)
print "Register ECAP1_TSCTR was " + hex(val)
val = _getReg(ECAP1_CTRPHS)
print "Register ECAP1_CTRPHS was " + hex(val)
val = _getReg(ECAP1_CAP1)
print "Register ECAP1_CAP1 was " + hex(val)
val = _getReg(ECAP1_CAP2)
print "Register ECAP1_CAP2 was " + hex(val)
val = _getReg(ECAP1_CAP3)
print "Register ECAP1_CAP3 was " + hex(val)
val = _getReg(ECAP1_CAP4)
print "Register ECAP1_CAP4 was " + hex(val)
val = _getReg(ECAP1_ECCTL1)
print "Register ECAP1_ECCTL1 was " + hex(val)
val = _getReg(ECAP1_ECCTL2)
print "Register ECAP1_ECCTL2 was " + hex(val)
val = _getReg(ECAP1_ECEINT)
print "Register ECAP1_ECEINT was " + hex(val)
val = _getReg(ECAP1_ECFLG)
print "Register ECAP1_ECFLG was " + hex(val)
val = _getReg(ECAP1_ECCLR)
print "Register ECAP1_ECCLR was " + hex(val)
val = _getReg(ECAP1_ECFRC)
print "Register ECAP1_ECFRC was " + hex(val)

print "Register EQEP1_QPOSCNT was " + hex(_getReg(EQEP1_QPOSCNT))
print "Register EQEP1_QPOSINIT was " + hex(_getReg(EQEP1_QPOSINIT))
print "Register EQEP1_QPOSMAX was " + hex(_getReg(EQEP1_QPOSMAX))
print "Register EQEP1_QPOSCMP was " + hex(_getReg(EQEP1_QPOSCMP))
print "Register EQEP1_QPOSILAT was " + hex(_getReg(EQEP1_QPOSILAT))
print "Register EQEP1_QPOSSLAT was " + hex(_getReg(EQEP1_QPOSSLAT))
print "Register EQEP1_QPOSLAT was " + hex(_getReg(EQEP1_QPOSLAT))
print "Register EQEP1_QUTMR was " + hex(_getReg(EQEP1_QUTMR))
print "Register EQEP1_QUPRD was " + hex(_getReg(EQEP1_QUPRD))
print "Register EQEP1_QWDTMR was " + hex(_getReg(EQEP1_QWDTMR))
print "Register EQEP1_QWDPRD was " + hex(_getReg(EQEP1_QWDPRD))
print "Register EQEP1_QDECCTL was " + hex(_getReg(EQEP1_QDECCTL))
print "Register EQEP1_QEPCTL was " + hex(_getReg(EQEP1_QEPCTL))





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


for timer in timers:
	print "Register TIDR was " + hex(_getReg(timer + 0x0))
	print "Register TIOCP_CONFIG was " + hex(_getReg(timer + 0x10))
	print "Register IRQ was " + hex(_getReg(timer + 0x20))
	print "Register IRQ was " + hex(_getReg(timer + 0x24))
	print "Register IRQ was " + hex(_getReg(timer + 0x28))
	print "Register IRQ was " + hex(_getReg(timer + 0x2c))
	print "Register IRQ was " + hex(_getReg(timer + 0x30))
	print "Register IRQ was " + hex(_getReg(timer + 0x34))
	print "Register TCLR was " + hex(_getReg(timer + 0x38))
	print "Register TCRR was " + hex(_getReg(timer + 0x3c))
	print "Register TLDR was " + hex(_getReg(timer + 0x40))
	print "Register TTGR was " + hex(_getReg(timer + 0x44))
	print "Register TWPS was " + hex(_getReg(timer + 0x48))
	print "Register TMAR was " + hex(_getReg(timer + 0x4c))
	print "Register TCAR1 was " + hex(_getReg(timer + 0x50))
	print "Register TSICR was " + hex(_getReg(timer + 0x54))
	print "Register TCAR2 was " + hex(_getReg(timer + 0x58))


