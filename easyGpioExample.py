from neo import Gpio
from time import sleep

pin = easyGpio(2) # Pin 2 with LED
readpin = easyGpio(3) # Pin 3 with switch

pin.pinOUT() # Make pin output 
readpin.pinIN() # Make pin in

while True:
	pin.on() # Turn pin on
	sleep(1) # wait one second
	pin.off() # Turn pin off
	print "pin 3 state %d" % readpin.get() # Get current pin state
	sleep(1)
