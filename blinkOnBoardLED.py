from machine import Pin
import time

led = Pin("LED", Pin.OUT)

def blinkForever(on,off):
    while True:
        led.on()
        time.sleep(on)
        led.off()
        time.sleep(off)
        
def blinkOnce(duration):
    led.on()
    time.sleep(duration)
    led.off()
    time.sleep(0.2)
    
def blinkNTimes(duration, n):
    for k in range(n):
        blinkOnce(duration)