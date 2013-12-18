echo am33xx_pwm > /sys/devices/bone_capemgr.7/slots

modprobe pwm_test

echo bone_pwm_P8_13 > /sys/devices/bone_capemgr.7/slots
echo bone_pwm_P8_19 > /sys/devices/bone_capemgr.7/slots

echo bone_pwm_P9_21 > /sys/devices/bone_capemgr.7/slots
echo bone_pwm_P9_22 > /sys/devices/bone_capemgr.7/slots

echo bone_pwm_P9_14 > /sys/devices/bone_capemgr.7/slots
echo bone_pwm_P9_16 > /sys/devices/bone_capemgr.7/slots

insmod mf2044-pwm-drv.ko
