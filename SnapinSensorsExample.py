# A library (example) to get the current values for the outboard sensors such as 
# Temperature sensor
# Barometer

from neo import Temp #import libraries
from neo import Barometer

from time import sleep # import for delays

temp = Temp() # init objects p.s. I auto initialize/reset the modules on these calls
baro = Barometer()

while True:
	tempVal = temp.getTemp("f") # replace f with c to get celcius
	print "Current temp from sensor 1: "+str(tempVal) #need to turn into string before building strings

	pressureVal = baro.getPressure() # gets the pressure in kPA
	print "Current pressure in (kPa):  "+str(pressureVal)

	tempFromBaro = baro.getTemp("c") # slower than temp sensor but still works same as temp sensor replace c with f for different modes
	print "Current temp from sensor 2: "+str(tempFromBaro)

	print "" # newline
	sleep(5) # wait a (5) second
