from mixer import Mixer
from time import sleep

mixer = Mixer()


def calibrate():
    print("#############################################################")
    print("#                 Pump calibration tool 1.0                 #")
    print("#############################################################\n")
    print("Calculates mixer.py max_spd value from multiple measurements.\n")

    results = []
    i = 0

    while True:
        x = input("Continue? (y/n)")
        if x == "n":
            break
        else:
            i = i+1
            qty = int(input("\nGive ml to pump: "))
            pump = int(input("Type pump number from 1 to 9: "))
            test = {pump: qty}

            mix_time = mixer.request(test)
            print(f"Pumping for {round(mix_time, 1)} seconds.")
            sleep(mix_time)
            result = int(input("Type result in ml: "))
            results.append(result/mix_time)
            print(f"Set max_spd output: {mixer.max_spd} ml/s")
            print(f"True max_spd output: {result / mix_time} ml/s\n")
    if i == 0:
        print("\nNo measurements done. Quitting...\n")
        quit()
    total = 0
    for value in results:
        total = value + total
    average = (total/i)+0.000001

    print("\n#############################################################")
    print(f"#         Suggested max_spd for mixer.py {round(average, 2)} ml/s          #")
    print("#############################################################\n")


if __name__ == "__main__":
    calibrate()
