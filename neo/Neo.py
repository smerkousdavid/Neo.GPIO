from os import system, devnull
from subprocess import call, STDOUT
from sys import exit
from time import sleep
from threading import Thread

class Gpio:
	def __init__(self):
		self.gpios = ["178", "179", "104", "143", "142", "141", "140", "149", "105", "148", "146", "147", "100", "102", "102", "106", "106", "107", "180", "181", "172", "173", "182", "124",
		"25", "22", "14", "15", "16", "17", "18", "19", "20", "21", "203", "202", "177", "176", "175", "174", "119", "124", "127", "116", "7", "6", "5", "4"]
		self.gpioval = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.gpiodir = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.current = 0
		self.OUTPUT = 1
		self.INPUT = 0
		self.HIGH = 1
		self.LOW = 0
		for num in self.gpios:
			try:
				with open("/sys/class/gpio/export", "w") as create:
					create.write(num)
				with open("/sys/class/gpio/gpio"+self.gpios[current]+"/value", "r") as reads:
					self.gpioval[self.current]=reads.read()
				with open("/sys/class/gpio/gpio"+self.gpios[current]+"/direction", "r") as readdir:
					self.gpiodir[self.current] = (1 if "out" in readdir.read() else 0)
				self.current += 1
			except:
				sleep(0.000001)
		print "Neo gpios started, make sure arduino isn't using the same pins or you can ruin this board!"

	def pinMode(self, pin=2, direction=0):
		try:
			gpio = self.gpios[int(pin)]
			if int(direction) != self.gpiodir[pin]:
				with open("/sys/class/gpio/gpio"+gpio+"/direction", "w") as writer:
					writer.write("in" if direction < 1 else "out")
				self.gpiodir[pin] = (0 if direction < 1 else 1)
			return True
		except ValueError:
			print "ERROR: pinMode, value inserted wasn't an int"
			return False
		except:
			print "ERROR: pinMode, error using pinMode"
			return False
			
	'''
	def pwmdonttouch(self, p, d):
		try:
			while True:
				t = open("/sys/class/gpio/gpio"+p+"/value", "w")
				t.write('1')
				t.close()
				sleep(d)
				t = open("/sys/class/gpio/gpio"+p+"/value", "w")
				t.write('0')
				t.close()
				sleep(d)
		except (KeyboardInterrupt, SystemExit):
			exit()
	def pwmWrite(self, pin=2, value = 0):
		try:
			with open("/sys/class/gpio/gpio"+self.gpios[int(pin)]+"/value", "r") as reads:
				check = reads.read()
			if "in" in check:
				print "Current pin direction is in"
				return False
			try:
				micro = (int(value)/100000)
				thread = Thread(target=self.pwmdonttouch, args=(self.gpios[int(pin)],micro,))
				#((self.pwms)[int(pin)]) = thread
				thread.start()
			except:
				print "ERROR: pwmWrite had a threading error"
		except ValueError:
			print "ERROR: pwmWrite, value inserted wasn't an int"
			return False
	'''		

	def digitalWrite(self, pin=2, value=0):
		try:
			gpio = self.gpios[int(pin)]
			if self.gpiodir[pin] != 1:
				with open("/sys/class/gpio/gpio"+gpio+"/direction", "w") as re:
					re.write("out")
				self.gpiodir[pin] = 1
			if self.gpioval[pin] != int(value):
				with open("/sys/class/gpio/gpio"+gpio+"/value", "w") as writes:
					writes.write("0" if value < 1 else "1")
				self.gpioval[pin] = (0 if value < 1 else 1)
			return True
		except ValueError:
			print "ERROR: digitalWrite, value inserted wasn't an int"
			return False
		except:
			print "ERROR: digitalWrite, error running"
			return False

	def digitalRead(self, pin=2):
		try:
			gpio = self.gpios[int(pin)]
			if self.gpiodir[pin] != 0:
				with open("/sys/class/gpio/gpio"+gpio+"/direction", "w") as re:
					re.write("in")
				self.gpiodir[pin] = 0
			with open("/sys/class/gpio/gpio"+gpio+"/value", "r") as reader:
				self.gpioval[pin] = int(reader.read().replace('\n',''))
			return self.gpioval[pin]
		except ValueError:
			print "ERROR: digitalRead, value inserted wasn't an int"
			return -1
		except:
			print "ERROR: digitalRead, error running"
			return -1

class Led:
	def __init__(self):
		self.led = 0

	def on(self):
		with open("/sys/class/leds/led0/brightness", "w") as w:
			w.write("1")

	def off(self):
		with open("/sys/class/leds/led0/brightness", "w") as w:
			w.write("0")

class Temp:
	def __init__(self): # Start temp module on object call
		self.temp = 0000
		NULLS = open(devnull, 'w')
		try:
			call(["rmmod", "lm75"], stdout=NULLS, stderr=STDOUT) # Reset module
		finally:
			sleep(0.0001) # wait for script update
		try:
			call(["modprobe", "lm75"], stdout=NULLS, stderr=STDOUT)
		finally:
			sleep(0.0001) # again script update		
		try:
			call(["echo", "lm75", "0x48", ">/sys/class/i2c-dev/i2c-1/device/new_device"], stdout=NULLS, stderr=STDOUT) #easier to run command to black hole using system
		finally:
			sleep(0.001) # longer script wait

	def getTemp(self, mode="f"): # Return with mode
		try:
			with open("/sys/class/i2c-dev/i2c-1/device/1-0048/temp1_input", "r") as reader: # Read i2c millicel file
				self.temp = (float(reader.read().replace(' ','').replace('\n', '')))*(0.001) # Turn into celcius
		except:
			print "Snap in sensor is not plugged in!"
		finally:
			return ((self.temp)*1.8+32) if "f" in mode else (self.temp) # Either return into Far or Celc

class Barometer:
	def __init__(self): 
		self.temp = 0000
		self.Tempscale = 0000
		self.pressure = 0000
		self.Tempress = 000
		NULLS = open(devnull, 'w')
		try:
			call(["rmmod", "mpl3115"], stdout=NULLS, stderr=STDOUT) # Reset module
		finally:
			sleep(0.0001) # wait for script update
		try:
			call(["modprobe", "mpl3115"], stdout=NULLS, stderr=STDOUT)
		finally:
			sleep(0.0001) # again script update		

	def getTemp(self, mode="f"): # Return from Barometer
		try:
			with open("/sys/class/i2c-dev/i2c-1/device/1-0060/iio:device0/in_temp_raw", "r") as treader:
				self.temp = (float(treader.read().replace('\n', '')))
			with open("/sys/class/i2c-dev/i2c-1/device/1-0060/iio:device0/in_temp_scale", "r") as tsreader:
				self.Tempscale = (float(tsreader.read().replace('\n', '')))
			self.temp = ((self.temp)*(self.Tempscale))
		except:
			print "Barometer is not plugged in!"
		finally:
			return ((self.temp)*1.8+32) if "f" in mode else (self.temp)

	def getPressure(self): # Return raw data which is (kPA) a form of pressure measurments sea level is about 100 
		try:
			with open("/sys/class/i2c-dev/i2c-1/device/1-0060/iio:device0/in_pressure_raw", "r") as preader:
				self.pressure = (float(preader.read().replace('\n', '')))
			with open("/sys/class/i2c-dev/i2c-1/device/1-0060/iio:device0/in_pressure_scale", "r") as psreader:
				self.Tempress = (float(psreader.read().replace('\n', '')))
		except:
			print "Barometer is not plugged in!"
		finally:
			return float((self.pressure)*(self.Tempress))
		
class Accel:
	def __init__(self): 
		self.accel = [0,0,0]
		self.raw = ""
		try:
			with open("/sys/class/misc/FreescaleAccelerometer/enable", "w") as enabler:
				enabler.write("1")
		except:
			print "Error: No Accel detected"

	def get(self): # Return accel data in array
		try:
			with open("/sys/class/misc/FreescaleAccelerometer/data", "r") as reader:
				self.raw= str(reader.read().replace('\n', ''))
			for a in range(0, 3):
				try:
					self.accel[a] = (int(self.raw[0:self.raw.index(',')]) if ',' in self.raw else int(self.raw))
					self.raw = self.raw[self.raw.index(',')+1:]
				except:
					break
		except:
			print "Error using accelerometer!"
		finally:
			return self.accel # return like this [x, y, z] in integer formats

class Magno:
	def __init__(self): 
		self.magn = [0,0,0]
		self.raw = ""
		try:
			with open("/sys/class/misc/FreescaleMagnetometer/enable", "w") as enabler:
				enabler.write("1")
		except:
			print "Error: No Magnometer detected"

	def get(self): # Return mango data in array
		with open("/sys/class/misc/FreescaleMagnetometer/data", "r") as reader:
			self.raw= str(reader.read().replace('\n', ''))
		for a in range(0, 3):
			try:
				self.magn[a] = (int(self.raw[0:self.raw.index(',')]) if ',' in self.raw else int(self.raw))
				self.raw = self.raw[self.raw.index(',')+1:]
			except:
				break
		return self.magn # return like this [x, y, z] in integer formats

class Gyro:
	def __init__(self): 
		self.gyro = [0,0,0]
		self.raw = ""
		try:
			with open("/sys/class/misc/FreescaleGyroscope/enable", "w") as enabler:
				enabler.write("1")
		except:
			print "Error: No Gyro detected"

	def get(self): # Return gyro data in array
		with open("/sys/class/misc/FreescaleGyroscope/data", "r") as reader:
			self.raw= str(reader.read().replace('\n', ''))
		for a in range(0, 3):
			try:
				self.gyro[a] = (int(self.raw[0:self.raw.index(',')]) if ',' in self.raw else int(self.raw))
				self.raw = self.raw[self.raw.index(',')+1:]
			except:
				break
		return self.gyro # return like this [x, y, z] in integer formats
