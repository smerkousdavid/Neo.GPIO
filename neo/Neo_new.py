from os import geteuid

from Maps import Maps
from Resources import MemoryMap, Command

if geteuid() != 0:
    print "Please run script as root!"
    exit(1)


class Gpio:
    def __init__(self):
        self.maps = Maps()
        self.export = open("/sys/class/gpio/export", "w")
        self.io_maps = [[None, None]] * (len(self.maps.gpios) + 1)

        for pin in range(0, len(self.maps.gpios)):
            try:
                cur_path = self.maps.get_gpio_path(pin)
                raw_pin = self.maps.gpios[pin]
                # self.export.resize(len(raw_pin))
                self.export.write(raw_pin)
                self.export.flush()
                self.io_maps[pin] = [MemoryMap(cur_path + "value", "r+"),
                                     MemoryMap(cur_path + "direction", "r+")]
            except (OSError, ValueError, IndexError, IOError, TypeError):
                try:
                    self.io_maps[pin][0].close()
                    self.io_maps[pin][1].close()
                except (TypeError, AttributeError):
                    pass
        print self.io_maps
        self.export.close()

    def pin_mode(self, pin, direction=0):
        try:
            self.io_maps[pin][1].write_line("in" if direction < 1 else "out")
        except (ValueError, IndexError, TypeError), e:
            print e
            raise ValueError("Current distribute %d" % pin)

    def digital_write(self, pin, value=0):
        try:
            self.io_maps[pin][0].write_digit(int(value > 0))
        except (ValueError, IndexError, TypeError):
            raise ValueError("Couldn't write %s to pin %s" % (str(value), str(pin)))

    def digital_read(self, pin):
        try:
            return self.io_maps[pin][0].read_digit(pin)
        except (ValueError, IndexError, TypeError):
            raise ValueError("Couldn't read state from pin %s" % str(pin))

    def release(self, pin):
        try:
            self.io_maps[pin][0].close(pin)
            self.io_maps[pin][1].close(pin)
        except (ValueError, IndexError, TypeError):
            raise ValueError("Couldn't release pin %s (Maybe already released)" % str(pin))


class EasyGpio(Gpio):
    def __init__(self, pin):
        self.pin = int(pin)
        Gpio.__init__(self)

    def pin_out(self):
        Gpio.pin_mode(self, self.pin, 1)

    def pin_in(self):
        Gpio.pin_mode(self, self.pin, 0)

    def on(self):
        Gpio.digital_write(self, self.pin, 1)

    def off(self):
        Gpio.digital_write(self, self.pin, 0)

    def get(self):
        return Gpio.digital_read(self, self.pin)


class Led:
    def __init__(self):
        self.led = 0
        self.mm_led = MemoryMap("/sys/class/leds/led0/brightness")

    def set(self, state=0):
        self.mm_led.write_digit(state)

    def on(self):
        self.mm_led.write_digit(1)

    def off(self):
        self.mm_led.write_digit(0)

    def get_state(self):
        return self.mm_led.read_digit()


class Temp:
    def __init__(self):  # Start temp module on object call
        self.temp = 0000
        self.coms = Command()
        try:
            self.coms.run("rmmod lm75")
        finally:
            pass
        try:
            self.coms.run("modprobe lm75")
        finally:
            pass
        try:
            self.coms.run("sh -c 'echo lm75 0x48 >/sys/class/i2c-dev/i2c-1/device/new_device' 2&>1")
            # easier to run command to black hole using system
        finally:
            pass
        self.mm_temp = MemoryMap("/sys/class/i2c-dev/i2c-1/device/1-0048/temp1_input")

    def get_temp(self, mode="f"):  # Return with mode
        try:
            self.temp = (float(self.mm_temp.read_line().replace(' ', '').replace('\n', ''))) * (
                0.001)  # Turn into celcius
        except (OSError, IndexError, IOError, ValueError):
            print "Snap in sensor is not plugged in!"
        finally:
            return (self.temp * 1.8 + 32) if "f" in mode else self.temp  # Either return into Far or Celc


from time import sleep

led = Gpio()
while True:
    led.pin_mode(2, 1)
    sleep(1)
    led.pin_mode(2, 0)
    sleep(1)
