# Neo.GPIO
#### A python library to control the Gpios, Accel, Gyro, Temp, Baro, Magno sensors/pins easily

## State of Neo.GPIO
-----------------
Given the fact that the Neo line from Udoo has been [discontinued](https://www.udoo.org/udoo-neo/), and there is no active support from Udoo, I will be archiving this repository for those who still have the boards like me, but I am not supporting it.

### Install
-----------------
To install this package just download the zip and extract the library anwhere your python file will be
EXAMPLE: place the neo folder on your desktop and then create a new python file on the desktop for your program

### Use
-----------------
#### INFO: you must run python file as root not udooer or errors might occur like sensor not plugged int<br>
Example on how to to run the files (You can replace the SnapinSensorsExample.py with whatever file you want to run):

```bash
echo udooer | sudo -S su -c 'python SnapinSensorsExample.py'
```
or<br>

```bash
echo udooer | sudo -S su -c 'python GpioExample.py'
```

To get started on the Neo use the examples that are provided in the zipped folder. For the Gpio use<br> 
Every pcb port number, which are labeled on the on the board itself<br>

If you don't want to look through the example files here is how to use them<br>

Create a new file outside of the neo folder called `gpio.py`<br><br>
Import the libraries<br>

```python
from neo import Gpio
from time import sleep
```

Associate with variables and create pins<br>
```python
gpio = Gpio()
writepin = 3
readpin = 2
```

Set each pin to certain direction (Input/Output)<br>
```python
gpio.pinMode(writepin, neo.OUTPUT)
gpio.pinMode(readpin, neo.INPUT)
```

Lets blink forever and read our second pin (Remember read pin must be pulled fully to either `LOW` or `HIGH` not hanging)<br>
```python
while True:
    gpio.digitalWrite(writepin, neo.HIGH)
    sleep(1)
    gpio.digitalWrite(writepin, neo.LOW)
    sleep(1)
    print "Pin 2 current state is: "+str(gpio.digitalRead(readpin))
```
Using a more object oriented approach
```python
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
```
Yaay if everything worked correctly and you wired the LED and input button correctly then you should be able to read and write values<br>
Remember GPIO is not the only thing you can do with this library you can use all the sensors that are provided currently for the Neo<br>Such as<br>
```python
Accel()
Gyro()
Magno()
Temp()
Barometer()
```
Check them out in the `SnapinSensorsExample.py` and `InBoardSensorsExample.py`<br>

### Other
-----------------
There is a lot of error checking that goes through before sending pin values<br>
The only thing that this won't handle is detecting is the cortex pins are on output, so if you set the cortex pin on output<br>
If you don't know what I mean, just to be safe flash the cortex with the minimal sketch so you don't damage the board<br>

Any questions? Contact me at smerkousdavid@gmail.com

