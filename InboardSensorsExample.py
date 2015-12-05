#Sensor examples for everything builtin the board such as 
#Magnometer -> Magnetic pull on device
#Gyroscope - > xyz tilt degree on the device
#Accelerometer -> xyz directional force measurment

from neo import Accel # import accelerometer
from neo import Magno # import magnometer
from neo import Gyro # import gyroscope

from time import sleep # to add delays

gyro = Gyro() # new objects p.s. this will auto initialize the device onboard
accel = Accel()
magno = Magno()

while True: # Run forever
	gyroVals = gyro.get() # Returns a full xyz list [x,y,z] realtime (integers/degrees)
	print "Gyroscope X: "+str(gyroVals[0])+" Y: "+str(gyroVals[1])+" Z: "+str(gyroVals[2])# turn current values (ints) to strings

	accelVals = accel.get() # Same as gyro return xyz of current displacment force
	print "Accelerometer X: "+str(accelVals[0])+" Y: "+str(accelVals[1])+" Z: "+str(accelVals[2])

	magnoVals = magno.get() # Above
	print "Magnometer X: "+str(magnoVals[0])+" Y: "+str(magnoVals[1])+" Z: "+str(magnoVals[2])

	print "" # newline
	sleep(1) # wait a second
