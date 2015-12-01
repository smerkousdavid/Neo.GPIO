from os import system, devnull
from sys import exit
from time import sleep
from threading import Thread
class Neo:
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
