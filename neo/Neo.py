from os import system, devnull
from sys import exit
from time import sleep
from threading import Thread
try:
	import numpy
except ImportError:
	print "Don't see numpy installed, installing now..."
	system("apt-get install python-numpy python-scipy ")
class Neo:
	def __init__(self):
		self.gpios = ["178", "179", "104", "143", "142", "141", "140", "149", "105", "148", "146", "147", "100", "102"]
		self.called = ""
		self.pwms = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
		for num in self.gpios:
			try:
				f = open("/sys/class/gpio/export", "w")
				f.write(str(num))
				f.close()
			except:
				sleep(0.0001)
		print "Neo gpios started, make sure arduino isn't using the same pins or you can ruin this board!"

	def pinMode(self, pin=2, direction=0):
		try:
			toWrite = ""
			if int(direction) == 0:
				toWrite = "in"
			elif int(direction) == 1:
				toWrite = "out"
			f = open("/sys/class/gpio/gpio"+self.gpios[int(pin)]+"/direction", "w")
			f.write(toWrite)
			f.close()
			return True
		except ValueError:
			print "ERROR: pinMode, value inserted wasn't an int"
			return False

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
			

	def digitalWrite(self, pin=2, value=0):
		try:
			with open("/sys/class/gpio/gpio"+self.gpios[int(pin)]+"/value", "r") as reads:
				check = reads.read()
			if "in" in check:
				print "Current pin direction is in"
				return False
			f = open("/sys/class/gpio/gpio"+self.gpios[int(pin)]+"/value", "w")
			f.write(str(int(value)))
			f.close()
			return True
		except ValueError:
			print "ERROR: digitalWrite, value inserted wasn't an int"
			return False
