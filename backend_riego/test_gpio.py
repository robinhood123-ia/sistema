import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

GPIO.output(17, GPIO.HIGH)
print("ENCENDIDO")
time.sleep(5)

GPIO.output(17, GPIO.LOW)
print("APAGADO")

GPIO.cleanup()
