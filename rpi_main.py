from gpiozero import Button, LED
import time, sys
from I2C_LCD_driver import lcd
from logic_statement import random_logical_expression, evaluate_logical_expression, random_bools


# User interface
lcd_screen = lcd()
lcd_screen.lcd_clear()

true_button = Button(20)
false_button = Button(21)

last_pressed_time = 0
debounce_time = 2.75

# Boolean indicator lights
x_true = LED(17)
y_true = LED(27)
z_true = LED(22)

x_false = LED(23)
y_false = LED(24)
z_false = LED(25)

# Binary score, written right to left
score_0 = LED(26)
score_1 = LED(19)
score_2 = LED(13)
score_3 = LED(6)
score_4 = LED(5)

# Master list of all LED objects for simple deactivation
bool_leds = [x_true, y_true, z_true, x_false, y_false, z_false]
score_leds = [score_0, score_1, score_2, score_3, score_4]

# Diagnostic print statements locating objects in memory:
bool_leds_str = ['x_true', 'y_true', 'z_true', 'x_false', 'y_false', 'z_false']
score_leds_str = ['score_0', 'score_1', 'score_2', 'score_3', 'score_4']

print("BOOL LEDs MEM LOC")
for leds, strings in zip(bool_leds, bool_leds_str):
    print(strings, leds)

print("SCORE LEDs MEM LOC")
for leds, strings in zip(score_leds, score_leds_str):
    print(strings, leds)

# Global variables indicating score, round start time, game activity, and initial boolean values
score = 0
start_time = 0
game_start = False
game_active = False
correct_answer = None
X = Y = Z = None

# Inner machinations (an enigma)
def get_new_string():
    '''
        Function: generates information necessary for one round and random truth values for X, Y, and Z
        Returns:
            expression (str), the logical expression in a human readable format
            answer (bool), the truth value of the overall expression given X, Y, and Z
    '''
    global X, Y, Z
    print("Trying to generate new expression")
    try:
        expression = random_logical_expression()
        X, Y, Z = random_bools()
        answer = evaluate_logical_expression(expression, X, Y, Z)
        return expression, answer
    except Exception as ex:
        print(f"Error in get_new_string, {ex}")

def update_progress_bar(time_left, total_time=30):
    '''
        Function: update_progress_bar, generates a string abstractly representing the time left in the round
        Args:
            time_left (int), the time in seconds remaining in the round
            total_time (int), total time allowed per round, defaults to 30s
        Returns:
            String of black boxes representing the fraction of time remaining in the round
    '''

    try:
        progress_length = 16
        filled_length = int(progress_length * time_left // total_time)
        black_box = chr(255)
        return black_box * filled_length + (" " * (progress_length - filled_length))
    except Exception as ex:
        print(f"Error in update_progress_bar: {ex}")

def update_bool_leds():
    '''
        Function: update_bool_leds, takes current set values for X, Y, and Z and turns true/false LEDs on or off accordingly
    '''
    global X, Y, Z
    print(f"Trying to update bool LEDS; X: {X}, Y: {Y}, Z: {Z}")
    try:
        [led.off() for led in bool_leds] # Turns off all bool LEDs
        if X != None: # If the program is in a game state
            
            print("X is True") if X else print("X is False") # Diagnostic print statement
            print("Y is True") if Y else print("Y is False")
            print("Z is True") if Z else print("Z is False")
            
            x_true.on() if X else x_false.on() # Turn true/false LEDs on accordingly
            y_true.on() if Y else y_false.on()
            z_true.on() if Z else z_false.on()
            
    except Exception as ex:
        print(f"Error in update_bool_leds: {ex}")

def get_led_states_from_score():
    '''
        Function: get_led_states_from_score, takes current score and converts it into states of individual LEDs in a binary display
        Returns: state_list (list), a list of Booleans indicating which LEDs are on and which are off to represent the score in binary 
    '''
    global score
    print(f"Trying to get LED states from score {score}")
    try:
        bin_score = f'{score:05b}' if score >= 0 else '00000'
        # Convert each binary digit to True (for '1') or False (for '0')
        state_list = [digit == '1' for digit in bin_score]
        print(f"Score LED state list {state_list} from score {bin_score}")
        return state_list

    except Exception as ex:
        print(f"Error in get_led_states_from_score: {ex}")

def update_score_leds():
    '''
        Function: update_score_leds, takes current score and displays it in binary on the score LEDS
    '''
    global score_leds, score
    print("Trying to update Score LEDs")
    try:
        [led.off() for led in score_leds]
        led_states = get_led_states_from_score()
        for led, digit in zip(reversed(score_leds), led_states): # list has to be reversed because the states read left to right
            print(str(led) + " on") if digit else print(str(led) + " off")
            led.on() if digit else led.off()
    except Exception as ex:
        print(f"Error in update_score_leads: {ex}")

def evaluate_response(is_correct):
    '''
        Function: changes global score depending on the correctness and timeliness of an answer
        Args:
            is_correct (bool), indicates whether or not the guess was correct
        Add'l Info:
            The scoring is based on time. If an answer is given in under ten seconds, it represents 3 points
            decrementing one point for every 10 seconds of play in a round. These points are given or taken
            away depending on whether the answer is correct or now. Once the answer has been evaluated, it
            resets the round state to prevent multiple presses from affecting the points awarded.
    '''
    global score, game_active, correct_answer, start_time
    print(f"Trying to evaluate button answer at time {time.time()}")
    print(f"Correct answer: {correct_answer}")
    print(f"Is correct: {is_correct}")
    try:
        if correct_answer != None:
            print("Pressed during an active game")
            print(f"Starting time: {start_time}")
            elapsed_time = time.time() - start_time
            print(f"Time elapsed: {elapsed_time}")
            if elapsed_time <= 10:
                points = 3
            elif elapsed_time <= 20:
                points = 2
            else:
                points = 1
            print(f"Points awarded: {points}")
            if is_correct:
                score += points
            else:
                score -= points
            print(f"Current score: {score}")
            game_active = False
            correct_answer = None
    except Exception as ex:
        print(f"Error in evaluate_response: {ex}")


def start_game():
    '''
        Function: start_game, main game loop
    '''
    global score, start_time, game_active, correct_answer
    score = 0
    rounds = 0
    game_active = True
    lcd_screen.lcd_clear()
    lcd_screen.lcd_display_string("GET READY", 1)
    time.sleep(2.6)
    while rounds < 10:
        rounds += 1
        print(f"ROUND {rounds} START")
        string_to_display, correct_answer = get_new_string()
        print(f"PROBLEM: {string_to_display}")
        print(f"CURRENT CORRECT ANSWER: {correct_answer}")
        lcd_screen.lcd_clear()
        time.sleep(0.1)
        print("DISPLAYING PROBLEM, UPDATING LEDs")
        lcd_screen.lcd_display_string(string_to_display, 1)
        
        update_bool_leds() # Update score/TF display
        update_score_leds()
        
        start_time = time.time() # Current time in seconds
        game_active = True # Global flag that marks the beginning and end of a round
        initial_score = score
        while game_active and time.time() - start_time < 30:
            time_left = 30 - (time.time() - start_time)
            lcd_screen.lcd_display_string(update_progress_bar(time_left), 2)
            time.sleep(0.1)
        if time.time() - start_time >= 30: # Lose points if the round ends without an answer
            print("TIMEOUT")
            score -= 1
        print(f"SCORE MARQUEE. SCORE: {score}")
        lcd_screen.lcd_clear()
        if initial_score < score:
            print("POINT GAINED")
            lcd_screen.backlight(0)
            time.sleep(0.2)
            lcd_screen.backlight(1)
            lcd_screen.lcd_display_string("CORRECT", 1)
            time.sleep(1)
            lcd_screen.lcd_display_string(f"Score: {score}", 2)
            time.sleep(1.5)
        else:
            print("POINT LOST")
            lcd_screen.backlight(0)
            time.sleep(0.2)
            lcd_screen.backlight(1)
            time.sleep(0.2)
            lcd_screen.backlight(0)
            time.sleep(0.2)
            lcd_screen.backlight(1)
            lcd_screen.lcd_display_string("WRONG", 1)
            time.sleep(1)
            lcd_screen.lcd_display_string(f"Score: {score}", 2)
            time.sleep(1)
        print(f"ROUND {rounds} OVER")

    # Game over logic
    lcd_screen.lcd_clear()
    print("ROUNDS OVER")
    lcd_screen.lcd_display_string("Game Over", 1)
    time.sleep(2)
    lcd_screen.lcd_display_string(f"Score: {score}", 2)
    time.sleep(5)

def true_pressed():
    '''
        Function: true_pressed, function executed when the True button is pressed at any point in the game
            correct_answer (bool), the current correct answer present in the round
            last_pressed_time (s), the last timepoint at which this button was pressed
                Offers a cooldown period between presses
                Debounce time is less than the interval between rounds 
    '''
    global correct_answer, last_pressed_time, game_start
    current_time = time.time()
    print("TRUE BUTTON PRESSED")
    if current_time - last_pressed_time > debounce_time:
        print("DEBOUNCE RESET FOR TB")
        last_pressed_time = current_time
        if correct_answer:  # correct_answer is True for an expression
            evaluate_response(True)
        else:
            evaluate_response(False)
        game_start = True

def false_pressed():
    '''
        Function: false_pressed, function executed when the False button is pressed at any point in the game
            correct_answer (bool), the current correct answer present in the round
            last_pressed_time (s), the last timepoint at which this button was pressed
                Offers a cooldown period between presses
                Debounce time is less than the interval between rounds 
    '''
    global correct_answer, last_pressed_time, game_start
    current_time = time.time()
    print("FALSE BUTTON PRESSED")
    if current_time - last_pressed_time > debounce_time:
        print("DEBOUNCE RESET FOR FB")
        last_pressed_time = current_time
        if not correct_answer:  # correct_answer is False for an expression
            evaluate_response(True)
        else:
            evaluate_response(False)
        game_start = True

# Setup button handlers
true_button.when_pressed = true_pressed
false_button.when_pressed = false_pressed

def cleanup_resources():
    '''
        Function: cleanup_resources, cleans up floating GPIO devices and I2C instance
    '''
    print("RELEASING RESOURCES")
    # Turn off all LEDs
    for led in bool_leds + score_leds:
        led.off()

    # Clear the LCD display
    lcd_screen.lcd_clear()

    # Clean up GPIO resources
    true_button.close()
    false_button.close()
    for led in bool_leds + score_leds:
        led.close()


# Main loop
try:
    lcd_screen.lcd_display_string("PRESS TO PLAY", 1)
    while True:
        time.sleep(0.1)
        if game_start:
            start_game()
            print("GAME OVER")
            game_start = False
            score = 0
            X = Y = Z = None
            correct_answer = None
            update_bool_leds()
            update_score_leds()
            lcd_screen.lcd_display_string("PRESS TO PLAY", 1)
            time.sleep(1)  # Prevent immediate restart

except KeyboardInterrupt:
    # Handle Ctrl+C interruption
    print("\nExiting gracefully...")
    cleanup_resources()
    sys.exit(0)
