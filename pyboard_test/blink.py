from pyb import LED, delay

led = LED(1)

while True:
    led.toggle()
    delay(100)
    