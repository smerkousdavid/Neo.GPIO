from os import geteuid
from time import sleep

from Maps import Maps
from Resources import MemoryMap, Command

if geteuid() != 0:
    print "Please run script as root! (If you are sudo it must be root\nLike this sudo su -c '<command>'"
    exit(1)

maps = Maps()
init_gpio = True
init_pwm = False
export_gpio = open(maps.gpio_export, "w")
export_pwm = open(maps.pwm_export, "w")
io_maps = [[None, None]] * (len(maps.gpios) + 1)
io_maps_pwm = [[None, None, None]] * (len(maps.pwms) + 1)


def re_map(value, omin, omax, nmin, nmax):
    return ((value - omin) /
            (omax - omin)) * (nmax - nmin) + nmin


class Gpio:
    def __init__(self, reset=False):
        if init_gpio or reset:
            for pin in range(0, len(maps.gpios)):
                try:
                    cur_path = maps.get_gpio_path(pin)
                    raw_pin = maps.gpios[pin]
                    # self.export.resize(len(raw_pin))
                    export_gpio.write(raw_pin)
                    export_gpio.flush()
                    io_maps[pin] = [MemoryMap(cur_path + "value"),
                                    MemoryMap(cur_path + "direction")]
                except (OSError, ValueError, IndexError, IOError, TypeError):
                    try:
                        io_maps[pin][0].close()
                        io_maps[pin][1].close()
                    except (TypeError, AttributeError):
                        pass
            export_gpio.close()

    @staticmethod
    def pin_mode(pin, direction=0):
        try:
            io_maps[pin][1].write_line("in" if direction < 1 else "out")
        except (ValueError, IndexError, TypeError), e:
            print e
            raise ValueError("Current distribute %d" % pin)

    @staticmethod
    def digital_write(pin, value=0):
        try:
            io_maps[pin][0].write_digit(int(value > 0))
        except (ValueError, IndexError, TypeError):
            raise ValueError("Couldn't write %s to pin %s" % (str(value), str(pin)))

    @staticmethod
    def digital_read(pin):
        try:
            return io_maps[pin][0].read_digit(pin)
        except (ValueError, IndexError, TypeError):
            raise ValueError("Couldn't read state from pin %s" % str(pin))

    @staticmethod
    def release(pin):
        try:
            io_maps[pin][0].close(pin)
            io_maps[pin][1].close(pin)
        except (ValueError, IndexError, TypeError):
            raise ValueError("Couldn't release pin %s (Maybe already released)" % str(pin))


class EasyGpio(Gpio):
    def __init__(self, pin, reset=False):
        self.pin = int(pin)
        Gpio.__init__(self, reset)

    def pin_out(self):
        Gpio.pin_mode(self.pin, 1)

    def pin_in(self):
        Gpio.pin_mode(self.pin, 0)

    def on(self):
        Gpio.digital_write(self.pin, 1)

    def off(self):
        Gpio.digital_write(self.pin, 0)

    def get(self):
        return Gpio.digital_read(self.pin)


class PWM:
    def __init__(self):
        self.period = 2040816  # Arduino default: 490Hz
        self.duty_cycle = 50  # Default

        for pin in range(0, len(maps.pwms)):
            try:
                cur_path = maps.get_pwm_path(pin)
                raw_pin = maps.pwms[pin]
                export_pwm.write(raw_pin)
                export_pwm.flush()
                io_maps_pwm[pin] = [MemoryMap(cur_path + "period"),
                                    MemoryMap(cur_path + "duty_cycle"),
                                    MemoryMap(cur_path + "enable")]
                io_maps_pwm[pin][0].write_line(str(self.period))
            except (OSError, ValueError, IndexError, IOError, TypeError):
                try:
                    io_maps_pwm[pin][0].close()
                    io_maps[pin][1].close()
                except (TypeError, AttributeError):
                    pass
        export_pwm.close()

    def set_period(self, pin=-1, frequency=2040816):
        self.period = frequency
        if pin != -1:
            io_maps_pwm[pin][0].write_line(str(self.period))
        else:
            for pins in range(0, maps.pwms):
                io_maps_pwm[pins][0].write_line(str(self.period))

    def pwm_write(self, pin, duty_cycle=50):
        min_val = int(0.1 * self.period)
        if duty_cycle == 0:
            io_maps_pwm[pin][1].write_digit(0)
        else:
            io_maps_pwm[pin][1].write_digit(1)
            new_val = re_map(duty_cycle, 0, 255, min_val, self.period)
            io_maps_pwm[pin][1].write_line(str(new_val))

    @staticmethod
    def pwm_read(pin):
        print "Function not available yet"

    @staticmethod
    def release(pin):
        try:
            io_maps_pwm[pin][0].close(pin)
            io_maps_pwm[pin][1].close(pin)
            io_maps_pwm[pin][2].close(pin)
        except (ValueError, IndexError, TypeError):
            raise ValueError("Couldn't release pin %s (Maybe already released)" % str(pin))


class Servo:
    def __init__(self):
        self.pwm_out = PWM()
        self.pwm_pin = 0
        self.pwm_min = 130
        self.pwm_max = 235
        self.angle_min = -90
        self.angle_max = 90
        self.servo_period = 20408163  # Typical servo works at 49Hz

    def attach(self):
        self.pwm_pin = 1
        self.set_period(self.servo_period)

    def set_period(self, servo_period=20408163):
        self.servo_period = servo_period
        self.pwm_out.set_period(self.pwm_pin, self.servo_period)

    def write(self, angle=0):
        angle = self.angle_min if angle < self.angle_min \
            else (self.angle_max if angle > self.angle_max else angle)
        pwm_write = re_map(angle, self.angle_min, self.angle_max, self.angle_min, self.angle_max)
        self.pwm_out.pwm_write(self.pwm_pin, pwm_write)

    def release(self):
        self.pwm_out.release(self.pwm_pin)


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
        self.mm_temp = MemoryMap("/sys/class/i2c-dev/i2c-1/device/1-0048/temp1_input", "r")

    def get_temp(self, mode="f"):  # Return with mode
        try:
            self.temp = (float(self.mm_temp.read_line().replace(' ', '').replace('\n', ''))) * (
                0.001)  # Turn into celcius
        except (OSError, IndexError, IOError, ValueError):
            print "Snap in sensor is not plugged in!"
        finally:
            return (self.temp * 1.8 + 32) if "f" in mode else self.temp  # Either return into Far or Celc


class Barometer:
    def __init__(self):
        self.temp = 0000
        self.Tempscale = 0000
        self.pressure = 0000
        self.Tempress = 000
        self.coms = Command()

        try:
            self.coms.run("rmmod mpl3115")
        finally:
            pass
        try:
            self.coms.run("modprobe mpl3115")
        finally:
            pass
        base = "/sys/class/i2c-dev/i2c-1/device/1-0060/iio:device0/"
        self.mm_temp = MemoryMap(base + "in_temp_raw", "r")
        self.mm_scale = MemoryMap(base + "in_temp_scale", "r")
        self.mm_pressure = MemoryMap(base + "in_pressure_raw", "r")
        self.mm_pressure_scale = MemoryMap(base + "in_pressure_scale", "r")

    def get_temp(self, mode="f"):  # Return from Barometer
        try:
            self.temp = (float(self.mm_temp.read_line().replace('\n', '')))
            self.Tempscale = (float(self.mm_scale.read_line().replace('\n', '')))
            self.temp = (self.temp * self.Tempscale)
        except (IndexError, ValueError, IOError, TypeError, OSError):
            print "Barometer is not plugged in!"
        finally:
            return (self.temp * 1.8 + 32) if "f" in mode else self.temp

    def get_pressure(self):  # Return raw data which is (kPA) a form of pressure measurments sea level is about 100
        try:
            self.pressure = (float(self.mm_pressure.read_line().replace('\n', '')))
            self.Tempress = (float(self.mm_pressure_scale.read_line().replace('\n', '')))
        except (IndexError, ValueError, IOError, TypeError, OSError):
            print "Barometer is not plugged in!"
        finally:
            return float(self.pressure * self.Tempress)

    def release(self, pin):
        try:
            self.mm_temp.close()
            self.mm_scale.close()
            self.mm_pressure.close()
            self.mm_pressure_scale.close()
        except (ValueError, IndexError, TypeError):
            raise ValueError("Couldn't release barometer" % str(pin))


class Accel:
    def __init__(self):
        self.accel = [0, 0, 0]
        self.calib = [0, 0, 0]
        self.valSub = []
        self.raw = ""
        try:
            with open("/sys/class/misc/FreescaleAccelerometer/enable", "w") as enabler:
                enabler.write("1")
                enabler.flush()
                enabler.close()
        except (OSError, IOError, ValueError, TypeError):
            print "Error: No Accel detected"

        self.mm_accel = MemoryMap("/sys/class/misc/FreescaleAccelerometer/data", "r")

    def calibrate(self, period=0.5):
        self.valSub = self.get()
        sum1 = [0, 0, 0]
        sum2 = [0, 0, 0]
        for num in range(0, len(self.accel)):
            sum1[num] = self.valSub[num]
        sleep(period)
        for num in range(0, len(self.accel)):
            sum2[num] = self.valSub[num]

        for num in range(0, len(self.accel)):
            self.calib[num] = (sum1[num] + sum2[num]) / 2

    def get(self):  # Return accel data in array
        try:
            self.raw = str(self.mm_accel.read_line().replace('\n', ''))
            for a in range(0, 3):
                try:
                    self.accel[a] = (int(self.raw[0:self.raw.index(',')]) if ',' in self.raw else int(self.raw))
                    self.raw = self.raw[self.raw.index(',') + 1:]
                except (IndexError, ValueError, TypeError):
                    break
        except (OSError, IOError, TypeError, ValueError):
            print "Error using accelerometer!"
        finally:
            for num in range(0, len(self.accel)):
                self.accel[num] -= self.calib[num]
            return self.accel  # return like this [x, y, z] in integer formats

    def release(self, pin):
        try:
            self.mm_accel.close()
            with open("/sys/class/misc/FreescaleAccelerometer/enable", "w") as enabler:
                enabler.write("0")
                enabler.flush()
                enabler.close()
        except (ValueError, IndexError, TypeError):
            raise ValueError("Couldn't release Accelerometer" % str(pin))


class Magno:
    def __init__(self):
        self.magn = [0, 0, 0]
        self.calib = [0, 0, 0]
        self.valSub = []
        self.raw = ""
        try:
            with open("/sys/class/misc/FreescaleMagnetometer/enable", "w") as enabler:
                enabler.write("1")
                enabler.flush()
                enabler.close()
        except (OSError, IOError, ValueError, TypeError):
            print "Error: No Magnometer detected"

        self.mm_magno = MemoryMap("/sys/class/misc/FreescaleMagnetometer/data", "r")

    def calibrate(self, period=0.5):
        self.valSub = self.get()
        sum1 = [0, 0, 0]
        sum2 = [0, 0, 0]
        for num in range(0, len(self.magn)):
            sum1[num] = self.valSub[num]
        sleep(period)
        for num in range(0, len(self.magn)):
            sum2[num] = self.valSub[num]

        for num in range(0, len(self.magn)):
            self.calib[num] = (sum1[num] + sum2[num]) / 2

    def get(self):  # Return mango data in array
        self.raw = str(self.mm_magno.read_line().replace('\n', ''))
        for a in range(0, 3):
            try:
                self.magn[a] = (int(self.raw[0:self.raw.index(',')]) if ',' in self.raw else int(self.raw))
                self.raw = self.raw[self.raw.index(',') + 1:]
            except (OSError, IOError, TypeError, IndexError, ValueError):
                break
        for num in range(0, len(self.magn)):
            self.magn[num] -= self.calib[num]
        return self.magn  # return like this [x, y, z] in integer formats

    def release(self, pin):
        try:
            self.mm_magno.close()
            with open("/sys/class/misc/FreescaleMagnetometer/enable", "w") as enabler:
                enabler.write("0")
                enabler.flush()
                enabler.close()
        except (ValueError, IndexError, TypeError):
            raise ValueError("Couldn't release Magnometer" % str(pin))


class Gyro:
    def __init__(self):
        self.gyro = [0, 0, 0]
        self.calib = [0, 0, 0]
        self.valSub = []
        self.raw = ""
        try:
            with open("/sys/class/misc/FreescaleGyroscope/enable", "w") as enabler:
                enabler.write("1")
                enabler.flush()
                enabler.close()
        except (OSError, IOError, ValueError, TypeError):
            print "Error: No Gyro detected"

        self.mm_gyro = MemoryMap("/sys/class/misc/FreescaleGyroscope/data", "r")

    def calibrate(self, period=0.5):
        self.valSub = self.get()
        sum1 = [0, 0, 0]
        sum2 = [0, 0, 0]
        for num in range(0, len(self.gyro)):
            sum1[num] = self.valSub[num]
        sleep(period)
        for num in range(0, len(self.gyro)):
            sum2[num] = self.valSub[num]

        for num in range(0, len(self.gyro)):
            self.calib[num] = (sum1[num] + sum2[num]) / 2

    def get(self):  # Return gyro data in array
        self.raw = str(self.mm_gyro.read_line().replace('\n', ''))
        for a in range(0, 3):
            try:
                self.gyro[a] = (int(self.raw[0:self.raw.index(',')]) if ',' in self.raw else int(self.raw))
                self.raw = self.raw[self.raw.index(',') + 1:]
            except (OSError, IOError, TypeError, IndexError, ValueError):
                break
        for num in range(0, len(self.gyro)):
            self.gyro[num] -= self.calib[num]
        return self.gyro  # return like this [x, y, z] in integer formats

    def release(self, pin):
        try:
            self.mm_gyro.close()
            with open("/sys/class/misc/FreescaleGyroscope/enable", "w") as enabler:
                enabler.write("0")
                enabler.flush()
                enabler.close()
        except (ValueError, IndexError, TypeError):
            raise ValueError("Couldn't release Magnometer" % str(pin))


led = Gpio()
while True:
    led.pin_mode(2, 1)
    sleep(1)
    led.pin_mode(2, 0)
    sleep(1)
