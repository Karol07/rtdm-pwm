import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM

GPIO.setup("P8_14", GPIO.OUT)
GPIO.output("P8_14", GPIO.HIGH)

PWM.start("P9_14", 35, 20000)
