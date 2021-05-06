import time
import RPi.GPIO as GPIO
import sys

class PumpConf:
    def __init__(self):
        self.SPEED_RATIO_SLOW = 3 / 40  # s/ml
        self.SPEED_RATIO_FAST = 3 / 100  # s/ml
        self.LIMIT_SLOW = 100  # ml
        self.SLOW_DC = 100  # %
        self.FAST_DC = 100  # %
        self.hz = 100

#        self.pins = [0, 1, 5, 6, 7, 8, 9, 10, 11]
        self.pins = [0, 1, 5, 6, 7, 9, 10, 11, 25]

        # Allocate necessary output pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pins, GPIO.OUT)

        self.pumps = {
          1: GPIO.PWM(0, self.hz),
          2: GPIO.PWM(1, self.hz),
          3: GPIO.PWM(5, self.hz),
          4: GPIO.PWM(6, self.hz),
          5: GPIO.PWM(7, self.hz),
          6: GPIO.PWM(25, self.hz),
          7: GPIO.PWM(9, self.hz),
          8: GPIO.PWM(10, self.hz),
          9: GPIO.PWM(11, self.hz),
        }

    # Map ingrediend amounts to pump times (two different pump speeds for over and under 100ml)
    def ml_to_pump_time(self, ml):
        ratio = self.SPEED_RATIO_SLOW if ml < self.LIMIT_SLOW else self.SPEED_RATIO_FAST
        return ml * ratio

    # Pump control function
    def make_drink(self, ingredients):
        """
        Controls the pumps to produce the drink defined by `ingredients`.
        :param ingredients: dictionary of ml per pump {pumpNo [int]: ml [int]}
        :return: None
        """
        # Timings
        max_time = max(map(lambda ingredient: self.ml_to_pump_time(ingredients[ingredient]), ingredients))
        start_time = time.time()
        cur_time = 0

        # Start all pumps with ingredients included in the recipe
        for ingredient in ingredients:
            dc = self.SLOW_DC if ingredients[ingredient] < self.LIMIT_SLOW else self.FAST_DC
            try:
                self.pumps[ingredient].start(dc)
            except:
                print("Ingredient required for recipe not configured!")
                raise

        # Run until last ingredient done
        while cur_time < max_time:
            # Check if pump has run long enough
            for ingredient in ingredients:
                # Stop pumps that have run long enough
                if self.ml_to_pump_time(ingredients[ingredient]) < cur_time:
                    self.pumps[ingredients[ingredient]].stop()

            time.sleep(0.1)
            cur_time = time.time() - start_time

if __name__ == '__main__':
    amount = 10
    pump = PumpConf()
    try:
#pump.make_drink({1: amount, 5: amount * 2})
#      pin = 7
#      GPIO.setmode(GPIO.BCM)
#      GPIO.setup(pin, GPIO.OUT)
#      pwm = GPIO.PWM(pin, 100)
#      pwm.start(100)
#      time.sleep(5)
#      pwm.stop()
#       pump.pumps[1].start(100)
#       pump.pumps[5].start(80)
#       time.sleep(2)
#       pump.pumps[1].stop()
#       pump.pumps[5].stop()
      print('kek')
    finally:
      GPIO.cleanup()
      sys.exit()
