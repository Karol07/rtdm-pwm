echo bone_eqep0 > /sys/devices/bone_capemgr.7/slots
echo bone_eqep1 > /sys/devices/bone_capemgr.7/slots
echo bone_eqep2 > /sys/devices/bone_capemgr.7/slots

modprobe tieqep
insmod ./mf2044-enc-drv.ko
