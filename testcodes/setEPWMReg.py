#! /usr/bin/python
from mmap import mmap
import struct

#L4_WKUP block in L3 memory map 
MMAP_OFFSET = 0x44c00000 
MMAP_SIZE   = 0x48ffffff-MMAP_OFFSET 

EPWM1 = 0x48302200 - MMAP_OFFSET #ePWM1, PWM Subsystem 1
EPWM2 = 0x48304200 - MMAP_OFFSET #ePWM2, PWM Subsystem 2

EPWM1_PCCTL = EPWM1 + 0x3c #offset 3Ch (P9_14)
EPWM2_PCCTL = EPWM2 + 0x3c #offset 3Ch (P8_19)

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

def _pwm_chpen(address, mask):
	_andReg(address,0x0)
	_orReg(address,mask)

def _pwm_oshtwth(address, mask):
	_andReg(address,0x0000 << 1)
	_orReg(address,mask << 1)

def _pwm_freq(address, mask):
	_andReg(address,0x000 << 5)
	_orReg(address,mask << 5)

def _pwm_duty(address, mask):
	_andReg(address,0x000 << 8)
	_orReg(address,mask << 8)

if __name__ == '__main__':
	print "EPWM1_PCCTL was " + hex(_getReg(EPWM1_PCCTL))
	print "EPWM2_PCCTL was " + hex(_getReg(EPWM2_PCCTL))

	_pwm_chpen(EPWM1_PCCTL,0x1)
	_pwm_chpen(EPWM2_PCCTL,0x1)

	_pwm_oshtwth(EPWM1_PCCTL,0x3)
	_pwm_oshtwth(EPWM2_PCCTL,0x15)

	_pwm_chfreq(EPWM1_PCCTL,0x3)
	_pwm_chfreq(EPWM2_PCCTL,0x5)

	_pwm_chduty(EPWM1_PCCTL,0x5)
	_pwm_chduty(EPWM2_PCCTL,0x6)

	print "EPWM1_CTL is changed: " + hex(_getReg(EPWM1_PCCTL))
	print "EPWM2_CTL is changed: " + hex(_getReg(EPWM2_PCCTL))

