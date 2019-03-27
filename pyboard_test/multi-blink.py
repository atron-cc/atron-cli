from pyb import LED, delay

leds = [
    LED(1),
    LED(2),
    LED(3),
    LED(4),
]

while True:
    for led in leds:
        led.toggle()
        delay(50)
    delay(100)
    