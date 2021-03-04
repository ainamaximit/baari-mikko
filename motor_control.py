import time
from time import sleep
from RPi.GPIO import GPIO

## Mockup stuff
recipes = [
    {
        "name": "vodka_battery",
        "ingredients": [
            ("vodka", 40),
            ("red_bull", 300)
        ]        
    },
    {
        "name": "jumalan_ruoska",
        "ingredients": [
            ("absintti", 40),
            ("jaloviina", 40)
        ]
    }
]

pump_configuration = {
    "vodka": 1,
    "jaloviina": 2,
    "absintti": 3,
    "red_bull": 4
}


## Constants
SPEED_RATIO_SLOW = 3000/40  # s/ml
SPEED_RATIO_FAST = 3000/100  # s/ml
LIMIT_SLOW = 100 # ml
SLOW_DC = 40 # %
FAST_DC = 100 # %


## Helpers
# Map ingrediend amounts to pump times (two different pump speeds for over and under 100ml)
def ml_to_pump_time(ml):
    ratio = SPEED_RATIO_SLOW if ml < LIMIT_SLOW else SPEED_RATIO_FAST
    return ml * ratio



## Initial setup
# Allocate necessary output pins
GPIO.setmode(GPIO.BCM)
for i in range(1, 18+1):
    GPIO.setup(i, GPIO.OUT)

# Create pump PWM instances
pumps = {}
for ing in pump_configuration:
    pumps[ing] = GPIO.PWM(pump_configuration[ing], 50)  # FIXME Does 50Hz work?


## Pump control function
# TODO Probably needs to be made async
def make_drink(recipe):
    # Timings
    max_time = max(map(lambda ing: ml_to_pump_time(ing[1]), recipe.ingredients))
    start_time = time.time()
    time = 0

    # Start all pumps with ingredients included in the recipe
    for ing in recipe.ingredients:
        dc = SLOW_DC if ing[1] < LIMIT_SLOW else FAST_DC
        try:
            pumps[ing].start(dc)
        except:
            print("Ingredient required for recipe not configured!")
            raise

    # Run until last ingredient done
    while time < max_time:
        # Check if pump has run long enough
        for ing in recipe.ingredients:
            # Stop pumps that have run long enough
            if ml_to_pump_time(ing[i]) < time:
                pumps[ing[0]].stop()

        sleep(100) # FIXME Is checking every 0.1 enough or too much?
        time = time.time() - start_time


