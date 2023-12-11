from gpiozero import Button, LED
from time import sleep
from I2C_LCD_driver import lcd

LED_pins = [17, 27, 22, 23, 24, 25, 26, 19, 13, 6, 5]
button_pins = [20, 21]
LED_objects = [LED(pin) for pin in LED_pins]
button_objects = [Button(pin) for pin in button_pins]

# screen = lcd()
'''
def test_display_string():
    print("Testing: Display String")
    screen.lcd_display_string("Testing Line 1", 1)  # Display on line 1
    sleep(3)
    screen.lcd_display_string("Testing Line 2", 2)  # Display on line 2
    sleep(5)  # Wait 5 seconds to visually check the display

# Function to test clearing the display
def test_clear_display():
    print("Testing: Clear Display")
    screen.lcd_clear()
    sleep(3)  # Wait 3 seconds to visually check the display

# Function to test backlight on and off
def test_backlight():
    print("Testing: Backlight On and Off")
    
    # Turn on the backlight
    print("Backlight On")
    screen.backlight(1)
    sleep(5)  # Wait 5 seconds to visually check the backlight

    # Turn off the backlight
    print("Backlight Off")
    screen.backlight(0)
    sleep(5)  # Wait 5 seconds to visually check the backlight
'''

def button_press():
    print("Button pressed")

try:
    while True:
        print("Trying to turn on Blue LEDs")
        for light in LED_objects:
            light.on()
            sleep(1)
            light.off()
except KeyboardInterrupt:
    print("Closing")
    [led.close() for led in LED_objects]

'''
test_backlight()
test_clear_display()
test_display_string()

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
'''
