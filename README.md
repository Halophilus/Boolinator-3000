# Boolinator-3000 - Documentation

![Boolinator Title](/docs/title.png)

## Table of Contents
1. [Introduction](#introduction)
2. [Key Features](#key-features)
3. [Hardware](#hardware)
    - [Components](#components)
    - [Case](#case)
    - [Circuit Design and Implementation](#circuit-design)
    - [Possible Revisions](#possible-revisions)
4. [Software](#software)
5. [Installation and Setup](#installation)
6. [Usage](#usage)
7. [Future Enhancements](#future-enhancements)
7. [Acknowledgements](#acknowledgements)
8. [Contact Information](#contact-information)
9. [License](#license)

## Introduction

![Demo image](/docs/readme/init.png)

This is the result of a final project in Dr. Alan Jamieson's CS 5002 Discrete Mathematics class. The premise is a simple logical game where users are given a mathematical statement (using NOT, AND, OR, and XOR logic) and the truth values of the variables therein, and the user has to evaluate the truth value of the overall statement. Over the course of one game, the user accrues a score as a collection of correct and incorrect answers, then the device offers the next game. The game combines an exploration of Boolean logic and a hardware-level user interface for a final product that is consistent and accurate.

## Key Features

Booting the Raspberry Pi automatically runs the script.

- **Game Loop**
    - The script starts and prompts the user on the screen to press a button to initate a game.
    - **Round**
        - A random mathematical statement using NOT (`!`), AND (`&`), OR (`|`), and XOR (`^`) logic is generated using the Boolean variables `X`, `Y`, and `Z`. This statement is then displayed on the screen.
        - Random truth values are assigned to `X`, `Y`, and `Z`.
            - These values are expressed to the user with LEDs per variable.
                - A Red LED turning on means False for that variable
                - Blue LED means True
        - A countdown timer bar begins gradually decrementing on the second row of the screen, representing a 30s timer.
        - The user is then prompted to press a button corresponding with the overall truth value of the statement.
            - Blue is True
            - Red is False
        - There is a scoring convention based on the amount of time taken to answer a question, adding for correct and subtracting for incorrect answers:
            - Less than 10s: 3 points
            - More than 20s: 2 points
            - Less than 30s: 1 point
            - More than 30s (no answer): -1 point
        - Accuracy of answer is evaluated:
            - Screen print of `CORRECT` or `WRONG` on first line.
            - Screen blinking.
                - Once for correct.
                - Twice for incorrect.
            - Current score is printed on the second line.
        - Score is represented on a binary display consisting of 5 yellow LEDs and updated.
            - `0` is off
            - `1` is on
            - Any score of 0 or lower appears as `00000`, or all off.
            - Maximum displayable score is 32, maximum possible score is 30, minimum possible score is -30.
    - The game continues for 10 rounds total.
    - The game then shows a `GAME OVER` screen with the score represented in decimal is printed on the second line
    - The game then returns to a `PRESS TO PLAY` mode with the score still visible on the screen and the binary display. 

---

## Hardware

### Components

| Component | Description | Notes | Quantity |
|---------|---------|---------|---------|
| Microcontroller | Raspberry Pi 2B+ | This project utilizes the gpiozero library for the Raspberry Pi, but can easily be adjusted for other microcontrollers. The output voltage will need to be safely stepped down to power LEDs. | 1 |
| USB PSU | Type-C USB 5V 2A Boost Converter Step-Up Power Module Lithium Battery Charging Protection Board | This serves to power not only the RPi, but also as an auxiliary power source to offset the current load from the RPi to independently power the LEDs. | 1 |
| I2C LCD Screen | RG1602A 16x2 Character LCD Display | Most directly compatible with the RPi, the size of the display limits the complexity of the statements generated | 1 |
| Switch | SPST Mini On/Off Toggle Switch | None | 1 |
| Resistor Set | 3 x 220ohm, 2 x 1Kohm, 11 x 10Kohm | 1/4W resistors needed | 15 |
| NPN Transistors | P2222 | These serve to control the PSU signal to the LEDs | 11 |
| Adapters | Pigtails to USB2.0 Male, Female USB to USB2.0 Male | This could theoretically be pigtails to micro-USB (these serve to power the RPi), but I had them separated for future versatility for different circuits. | 2 |
| Wiring | 16awg solid-core copper wire, 12awg raw copper wire | Components that are primarily rigid can use these rigid wires. Solid-core wires can be color-coded. Raw copper wire needs to be insulated in some way from other sensitive electrical components, such as the underside of the RPi. | 5ft. each |
| Jumpers | Multicolored male-to-male, female-to-female, and male-to-female | These are primarily used for wires that connect separate rigid components and form impermanent connections, such as for attaching circuits to pins that might be removed or rearranged. This allowed for flexibility during debugging and incremental testing of each component. In the case of the transistor arrays, these jumper leads were soldered directly to the boards for flexible connections. The color differences also afford clarity in circuit design. | 20 each |
| LEDs | 5mm, Blue, Red, and Yellow | Sometimes during testing, these burn out, so order plenty of extras. Keep in mind that different color LEDs have different threshold voltages, and depending on the power of the PSU board, high current loads may result in a voltage drop below that which might be required for certain LEDs. This happened with the blue LEDs in this project. | 10 each | 
| Buttons | Blue and Red SMD Momentary Tactile Pushbuttons | The tactile effect is crucial for the game experience. Always run these through a limiting resistor in case of an accidental signal through the button. | 2 |
| Protoboards | Solderable Circuit Prototyping Boards | The transistor arrays and the voltage divider were built on these and could be easily stored within the case despite not having a space. These can provide a rigid platform for wiring that might be brittle. | 5 |
| Battery | 3.7V Li-Po Battery | The size of this battery isn't particularly important, as the current draw for this device is insignificant. Still, 1000 mAh are recommended. | 1 | 

---

### Case

![Lid 3D Model](/docs/readme/lid.png)

- **Lid**:
    - The lid was designed to accommodate:
        - 5mm LEDs
            - 3 Blue LEDs indicating True for `X`, `Y`, and `Z`.
            - 3 Red LEDS indicating False for `X`, `Y`, and `Z`.
            - 5 Yellow LEDs each indicating a digit for the 5-digit
        - 12x12x7.5mm Buttons
        - Generic RG1602A Screens
            - The lid contains a recessed edge on the reverse to allow the screen to jut out of the face of the lid.
    - There are labels in relief:
        - Columns: Sets of True and False LEDs
        - Rows: True or False value associated with each variable.
    - There are three screw posts to mount the Raspberry Pi on the reverse of the lid.
        - The pins face down, opposite the face of the lid.
        - The main body of the case has enough space to accommodate the pins and wires wrapping around to connect to the pin.
        - There is enough negative space store all circuit boards comfortably, despite the fact that they are free floating.
        - The posts take 2.5M screws.
    - Buttons have retaining support structures so there is a brace for consistent button presses.
    - The lid has no fixing features so that the device can easily be opened to show off the circuitry.

![Lid with RPi Installed](/docs/readme/lid_demo.png)

---

![Case Body Model](/docs/readme/body.png)

- **Body**
    - The primary purpose of the case's body to provide space to store the additional hardware
    - A slot on the top-left corner permits enough clearance for the USB C port from the boost converter to reach the outside.
    - Four posts are present to support and set the LCD screen in place.
    - The battery and power-related circuits fit underneath the screen.
    - The remaining transistor arrays can fit underneath the RPi.

![Body with Screen Installed](/docs/readme/screen.png)

- **Additional Modifications**
    - The power switch was passed through a hole that was drilled in the side post-fab.
    - Buttons and LEDs are glued into place to prevent them from moving around.
    - A hole in the side was dremeled out to allow for space for the power cord when powering through the 5V rails on the RPi failed.
    - The boost converter can be glued into place for fitment.

![Bent wire detail with exposed charging port](/docs/readme/detail.jpeg)

---

### Circuit Design

#### Power Supply

![Labeled components related to supplying power](/docs/readme/power_img.png)

1. 5V Boost Converter and Battery Charging Board
    - Can be given auxiliary power as a passthrough for 5V from USB.
    - Can also be powered with a 3.7V LiPo for portability.
    - Produces 5V on dedicated rails and on USB leads.
    - Can be triggered to an on-stae by introducing a resistive load.
    - A lower trickle current will keep the power supply active, so any additional current sourcing must be cut off all at once.
    - Higher current limits than the 5V rails on an RPi.

2. Transistor-Based Voltage-Divider Cut-Off
    - The voltage divider draws a trickle current even when the RPi is switched off.
    - This will maintain an on state for the boost converter, draining power.
    - This cuts power from the voltage divider when the RPi is off.

3. Voltage Divider:
    - The 5V rails on the boost converter are used to power the LEDs to reduce current sourcing from the RPi.
    - 5V is too high for the operating range of the LEDs, so a voltage divider is used to step this voltage down to 3.3V.

4. SPST Toggle Switch
    - This bridges the power from the USB OUT rails on the boost converter to the Micro USB cable powering the RPi.
    - The suddent resistive load triggers the boost converter to turn on and power the RPi.
    - A lead on the neutral side of the switch connects to the cut-off transistor.
    - When switched on, this positive signal triggers the gate of the transistor and opens the voltage divider circuit to the boost converter.

5. LiPo Battery
    - Completely unnecessary, but was useful when doing the presentation for this project.
    - Circuit can exist totally off of wired power.
    - The battery was stored in an anti-static bag to insulate the leads from stray wires

**Circuit Diagram**

![Power Supply Diagram](/docs/readme/power.png)

- **USB**: 5V Boost Converter
- **BATT**: 3.7V LiPo Battery
- **SPST**: Toggle Switch
- **RPi**: Raspberry Pi (USB)
- **Q1**: Resistor Cut-Off
- **R1**: 220ohm, can theoretically be any resistance below 500 as the ratio of the 3 involved resistors will always divide the voltage to 3.3V at the 3.3V node. Resistances over 500 will limit the current too much.
- **LEDs**: all LEDs on the face of the device.
- All devices are connected to a common ground

![Common for LEDs and Buttons](/docs/readme/reverse_lid.jpg)

An insulating layer of plastic is added between the copper wire and the RPi to avoid shorts.

---

#### Transistor Arrays

![8-Bit Transistor Array](/docs/readme/array_img.JPEG)

- To reduce the current draw from the RPi when powering the LEDs, these arrays were created.
- Instead of drawing 10-20mA per LED from the RPi, this system reduces that current to 1-2mA.
- Theoretically, this should reduce current sourcing from the RPi.
- One side (the thumb side), takes in a GPIO input to the gate of the transistor.
- The other side provides 3.3V when the GPIO is high.
- The source posts are all joined in parallel and wired to the voltage divider.

**Circuit Diagram**

![Transistor Array Node](/docs/readme/transistor.png)

- Each node in the transistor consists of this circuit.
- **DIV**: Voltage source taken at center node in voltage divider.
- **R1**: 2N2222 take very little current to activate, so a 10Kohm resistor is allowable here.

![An early circuit prototype](/docs/readme/prototype.png)

---

### Possible Revisions

- The biggest bug in this design is that when the device is under load, the blue LEDs do not turn on. Everything else works.
- This is likely due to the voltage drop and the higher operating voltage of the blue LEDs I used.
- One possible solution is to power only the blue LEDs via GPIO to reduce the current drop.
- The overall current sourcing would still be within acceptable limits for the whole device.

---

## Software

The function of the game is driven by three primary scripts, `logic_statement.py`, `rpi_main.py`, and `I2C_LCD_Driver.py`. The code for `I2C_LCD_Driver.py` was provided by [Denis Pleic](https://gist.github.com/DenisFromHR/cc863375a6e19dce359d) and serves as a driver for the LCD display.

### logic_statement.py
    - Generates a random mathematical statement
    - Assigns truth values to variables in that statement.
    - Evaluates the overall truth value for the statement

### rpi_main.py
    - Executes logic of the game

---

## Installation

1. Install the latest version of Raspberry Pi OS.
    - Configure the OS to have the login details for your local network so that it automatically connects.
    - Ensure that the distribution is up to date by running this in the terminal after initial startup:
    ```bash
    sudo apt-get update
    sudo apt-get upgrade
    ```
2. Clone the `Boolinator-3000` git repository.
```bash
cd /path
git clone https://github.com/Halophilus/Boolinator-3000.git
cd /Boolinator-3000
```
3. Use `crontab` to schedule `rpi_main.py` to load on boot.
    - Open the Crontab file for editing
    ```bash
    sudo crontab -e
    ```
    - Assume that `/path` represents the chosen directory for the git repository
    ```bash
    @reboot /usr/bin/python3 /path/Boolinator-3000/rpi_main.py
    ```
    - Save and exit: press `ctrl + x` then `y` then `enter`.
    - Check to see if the new cronjobs have been added:
    ```bash
    crontab -l
    ```
4. Ensure that each file has execute permissions with the following command:
    ```bash
    sudo chmod +x /path/Boolinator-3000/rpi_main.py
    ```
5. Enable I2C LCD Displays in `raspi-config`
    - Run `sudo raspi-config` in the terminal
    - Navigate to `Interfacing Options`
    - Select `I2C` and choose `<Yes>`
    - Exit `raspi-config`
    - Verify that I2C is enabled by running the following:
    ```bash
    lsmod | grep i2c
    ```
6. Attach each lead for each input/output device to a corresponding GPIO.
    - The SDA and SCL pins that bus display information to the I2C display are GPIO 2 and 3 respectively.
    - The I2C display is powered by the 5V RPi rails.
    - The LED and Button pins can be assigned to any remaining available pins, as long as the numbers correspond to the script.
    - **Default Pin Assignment**:
        - True LEDs:
            - X: 17
            - Y: 27
            - Z: 22
        - False LEDs:
            - X: 23
            - Y: 24
            - Z: 25
        - Score LEDs (left to right): 26, 19, 13, 6, 5
        - True Button: 20
        - False Button: 21
7. Reboot the device. The game should then start upon every reboot.



## Usage

The game will play automatically on startup. Once a game is finished, it will display the final score. This can be repeated indefinitely. High scores can be manually kept track of.

## Future Enhancements

- A high score system
- Buzzer sound feedback
- Fix for blue LEDs

## Acknowledgements

Credit to [Denis Pleic](https://gist.github.com/DenisFromHR/cc863375a6e19dce359d) for `I2C_LCD_driver.py` and special thanks to Dr. Alan Jamieson for the excuse to do this project.

## Contact Information

For any questions regarding replicating this project, please contact [Halophilus](benshaw@halophil.us)

## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE file](LICENSE.txt) for details.
