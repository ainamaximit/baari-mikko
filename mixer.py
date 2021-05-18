import time
import RPi.GPIO as GPIO
from threading import Thread


class Mixer:
    def __init__(self):
        self.max_spd = 7.66  # 460 ml/min (7,66 ml/s) needs calibration
        self.min_spd = 0  # 46 ml/min (0,766 ml/s) needs calibration

        self.pinLayout = {1: 1, 2: 26, 3: 19, 4: 6, 5: 7, 6: 25, 7: 9, 8: 10, 9: 11}
        self.pumps = {}
        self.freq = 100

        # Configure pumps
        GPIO.setmode(GPIO.BCM)
        for key, value in self.pinLayout.items():
            GPIO.setup(value, GPIO.OUT)
            self.pumps[key] = GPIO.PWM(value, self.freq)
            self.pumps[key].start(0)

    def mix(self, recipe, min_time):
        """

        :param recipe:
        :param min_time:
        :return:
        """
        for key, value in recipe.items():
            target = (((value / min_time) - self.min_spd) / (self.max_spd - self.min_spd)) * 100
            print(f"{key}:{target}")
            recipe[key] = target

        for key, value in recipe.items():
            self.pumps[key].ChangeDutyCycle(value)
            print(f"{self.pumps[key]} pwm cycle to {value}")

        time.sleep(min_time)
        print("Pausing pumps...")

        for key, value in self.pumps.items():
            self.pumps[key].ChangeDutyCycle(0)
            print(f"{key} pwm cycle to 0")

    def request(self, recipe):
        """
        Calculate pump duty cycles from recipe and run all pumps for same time.
        :param recipe: dict. Drink recipe.
        :return: Time it takes to mix.
        """
        try:
            most_qty = recipe[max(recipe, key=recipe.get)]
            print(f"Largest dose for one pump: {most_qty}ml")
            min_time = most_qty/self.max_spd
            print(f"Takes {min_time} seconds to make.")
            print("Running pumps")
        except Exception as e:
            print(f"mixer.py: Error in recipe parsing. {e}")
        else:
            t = Thread(target=self.mix, args=(recipe, min_time))
            t.start()
            return min_time

    def stop(self):
        try:
            for key, _ in self.pumps.items():
                self.pumps[key].stop()
                print(f"Pump {key} stopped.")
        except Exception as e:
            print(f"mixer.py: Error Stopping pumps. {e}")
        finally:
            GPIO.cleanup()
            print("Pin allocation cleaned.")


if __name__ == "__main__":
    # recipe = {3: 50, 6: 50, 9: 100}
    recipe = {5: 10}

    mixer = Mixer()
    asd = mixer.request(recipe)
    print(asd)
