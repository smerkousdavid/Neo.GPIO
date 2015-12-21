from neo import Led
from time import sleep

led = Led()

while True:
	led.on() # Turn Led on (red)
	sleep(1) # wait one second
	led.off() # Turn Led off
	sleep(1)
