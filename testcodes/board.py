import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import subprocess

GPIO.setup("P8_14", GPIO.OUT)
GPIO.output("P8_14", GPIO.HIGH)
#GPIO.cleanup()
#GPIO.output("P8_10", GPIO.LOW)

#PWM.start("P9_14", 25, 40000)
#PWM.start("P9_14", 25, 4000)

subprocess.call("./mf2044-pwm-test")
#subprocess.call("./mf2044-enc-test")

#PWM.set_duty_cycle("P9_14", 35)
#PWM.set_frequency("P9_14", 20000)
