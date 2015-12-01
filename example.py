#Library and example created by David Smerkous

from neo import Neo #import neo.gpio library
from time import sleep #like the delay function

neo = Neo() #create new Neo object

pinTwo = 2 #pin to use
pinThree = 3

neo.pinMode(pinTwo, neo.OUTPUT)# Use innerbank pin 2 and set it as output either 0 (neo.INPUT) or 1 (neo.OUTPUT)
neo.pinMode(pinThree, neo.INPUT)# Use pin three(innerbank) and read set state to read

#Blink example
for a in range(0, 10): #Do for ten times
	neo.digitalWrite(pinTwo,neo.HIGH) #write high value to pin
	sleep(1)# wait one second
	neo.digitalWrite(pinTwo,neo.LOW) #write low value to pin
	sleep(1)# wait one second

#Read pin
print "Current pin("+pinThree+") state is: "+str(neo.digitalRead(pinThree)) # read current value of pinThree
