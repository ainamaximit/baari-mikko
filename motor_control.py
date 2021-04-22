import time
import RPi.GPIO as GPIO


class PumpConf:
    def __init__(self):
        self.SPEED_RATIO_SLOW = 3000 / 40  # s/ml
        self.SPEED_RATIO_FAST = 3000 / 100  # s/ml
        self.LIMIT_SLOW = 100  # ml
        self.SLOW_DC = 40  # %
        self.FAST_DC = 100  # %

        self.hz = 100
        self.pumpCount = 9
        self.pumps = {}

        # Allocate necessary output pins
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        for i in range(1, self.pumpCount + 1):
            GPIO.setup(i, GPIO.OUT)
            self.pumps[1] = GPIO.PWM(i, self.hz)

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
