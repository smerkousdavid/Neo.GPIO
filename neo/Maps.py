class Maps:
    def __init__(self):
        self.gpios = ["178", "179", "104", "143", "142", "141", "140", "149", "105", "148", "146", "147", "100", "102",
                      "102", "106", "106", "107", "180", "181", "172", "173", "182", "124",
                      "25", "22", "14", "15", "16", "17", "18", "19", "20", "21", "203", "202", "177", "176", "175",
                      "174", "119", "124", "127", "116", "7", "6", "5", "4"]

        self.pwms = ["0", "1", "2", "3", "4", "5", "6"]

        self.OUTPUT = 1
        self.INPUT = 0
        self.HIGH = 1
        self.LOW = 0

        self.pwm_export = "/sys/class/pwm/pwmchip0/export"
        self.gpio_export = "/sys/class/gpio/export"

    def get_gpio_path(self, gpio_num):
        return "/sys/class/gpio/gpio%s/" % self.gpios[gpio_num]

    def get_pwm_path(self, pwm_num):
        return "/sys/class/pwm/pwmchip0/pwm%s/" % self.pwms[pwm_num]
