import RPi.GPIO as GPIO
import time

class  R2R_ADC:
    def __init__(self, dynamic_range, compare_time = 0.01, verbose = False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial = 0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def deinit(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()

    def number_to_dac(self, number):
        bn = [int(element) for element in bin(number)[2:].zfill(8)]
        for i in range(len(self.bits_gpio)):
            GPIO.output(self.bits_gpio[i], bn[i])

    def sequential_counting_adc(self):
        for value in range(256):
            self.number_to_dac(value)
            time.sleep(self.compare_time)
            comparatorValue = GPIO.input(self.comp_gpio)
            if comparatorValue == 1:
                return value
        return 255

    def get_sc_voltage(self):
        return self.sequential_counting_adc() / 255 * self.dynamic_range

    def successive_approximation_adc(self):
        l = -1
        r = 255
        while r - l != 1:
            m = (l + r) // 2
            self.number_to_dac(m)
            time.sleep(self.compare_time)
            if GPIO.input(self.comp_gpio) == 1:
                r = m
            else:
                l = m
        return r

    def get_sar_voltage(self):
        return self.successive_approximation_adc() / 255 * self.dynamic_range

if __name__ == '__main__':
    try:
        adc = R2R_ADC(3.21)

        while True:
            #print(adc.get_sc_voltage())
            print(adc.get_sar_voltage())

    finally:
        adc.deinit()