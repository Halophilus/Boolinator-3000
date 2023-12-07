from gpiozero import Button, LED
from time import sleep
LED_pins = [14, 15, 18, 23, 24, 25]
adder_pins = [9, 11, 0, 5, 6, 13, 19, 25]
button_pins = [20, 21]

LED_objects = [LED(pin) for pin in LED_pins]
adder_objects = [LED(pin) for pin in adder_pins]
button_objects = [Button(pin) for pin in button_pins]

def button_press():
    print("Button pressed at pin!")

for signal in adder_objects:
    signal.on()
    sleep(1)
    signal.off()

for light in LED_objects:
    signal.on()
    sleep(1)
    light.off()

for button in button_objects:
    button.when_pressed = button_press(button.pin.number)

for button in button_objects:
    for signal in adder_objects:
        print(f"Waiting for button press at pin {signal.pin.number}")
        signal.on()
        button.wait_for_press()
        signal.off()
        sleep(1)
    for light in LED_objects:
        print(f"Waiting for button press at pin {light.pin.number}")
        light.on()
        button.wait_for_press()
        light.off()
        sleep(1)
    
