from gpiozero import Button, LED
import time
from I2C_LCD_driver import lcd
from logic_statement import random_logical_expression, evaluate_logical_expression, random_bools

# User interface
lcd_screen = lcd()
true_button = Button(20)
false_button = Button(21)

# Boolean indicator lights
x_true = LED(14)
y_true = LED(15)
z_true = LED(18)

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

# Global variables indicating score, round start time, game activity, and initial boolean values
score = None
start_time = 0
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
        return black_box * filled_length + ("-" * (progress_length - filled_length))
    except Exception as ex:
        print(f"Error in update_progress_bar: {ex}")

def update_bool_leds():
    '''
        Function: update_bool_leds, takes current set values for X, Y, and Z and turns true/false LEDs on or off accordingly
    '''
    global X, Y, Z
    try:
        [led.off() for led in bool_leds] # Turns off all bool LEDs
        if X != None: # If the program is in a game state
            print("X is True") if X else print("X is False") # Turn true/false LEDs on accordingly
            print("Y is True") if Y else print("Y is False") # Turn true/false LEDs on accordingly
            print("Z is True") if Z else print("Z is False") # Turn true/false LEDs on accordingly
            '''
            x_true.on() if X else x_false.on() # Turn true/false LEDs on accordingly
            y_true.on() if Y else y_false.on()
            z_true.on() if Z else z_false.on()
            '''
    except Exception as ex:
        print(f"Error in update_bool_leds: {ex}")

def get_led_states_from_score():
    '''
        Function: get_led_states_from_score, takes current score and converts it into states of individual LEDs in a binary display
        Returns: state_list (list), a list of Booleans indicating which LEDs are on and which are off to represent the score in binary 
    '''
    global score
    try:
        state_list = []
        bin_score = bin(score)[2:] # Slice clips off leading base
        for digit in bin_score: # For every binary digit in the score
            if digit == "1":
                state_list.append(True) # Light goes on to indicate a 1
            else:
                state_list.append(False) # Light goes off to indicate a 0
        return state_list
    except Exception as ex:
        print(f"Error in get_led_states_from_score: {ex}")

def update_score_leds():
    '''
        Function: update_score_leds, takes current score and displays it in binary on the score LEDS
    '''
    global score_leds, score
    try:
        [led.off() for led in score_leds]
        if score != None:
            led_states = get_led_states_from_score()
            for led, digit in zip(reversed(score_leds), led_states): # list has to be reversed because the states read left to right
                print(str(led) + " on") if digit else print(str(led) + " off")
                # led.on() if digit else led.off()
    except Exception as ex:
        print(f"Error in update_score_leads: {ex}")

def flash_screen():
    lcd_screen.backlight(0)
    time.sleep(0.2)
    lcd_screen.backlight(1)

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
    global score, game_active
    try:
        elapsed_time = time.time() - start_time
        if elapsed_time <= 10:
            points = 3
        elif elapsed_time <= 20:
            points = 2
        else:
            points = 1
        if is_correct:
            score += points
            flash_screen()
        else:
            score -= points
            flash_screen()
        game_active = False
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

    while rounds < 10 and score < 32 and score >= 0:
        rounds += 1
        string_to_display, correct_answer = get_new_string()
        
        lcd_screen.lcd_clear()
        lcd_screen.lcd_display_string(string_to_display, 1)
        
        update_bool_leds() # Update score/TF display
        update_score_leds()
        
        start_time = time.time() # Current time in seconds
        game_active = True # Global flag that marks the beginning and end of a round

        while game_active and time.time() - start_time < 30:
            time_left = 30 - (time.time() - start_time)
            lcd_screen.lcd_display_string(update_progress_bar(time_left), 2)
            time.sleep(0.1)

        if time.time() - start_time >= 30:
            score -= 1  # Lose points if the round ends without an answer

    # Game over logic
    lcd_screen.lcd_clear()
    lcd_screen.lcd_display_string("Game Over", 1)
    time.sleep(2)
    lcd_screen.lcd_display_string(f"Score: {score}", 2)
    time.sleep(5)

def true_pressed():
    global correct_answer
    if correct_answer:  # correct_answer is True for an expression
        evaluate_response(True)
    else:
        evaluate_response(False)

def false_pressed():
    global correct_answer
    if not correct_answer: # correct_answer is False for an expression
        evaluate_response(True)
    else:
        evaluate_response(False)

# Setup button handlers
true_button.when_pressed = true_pressed
false_button.when_pressed = false_pressed

# Main loop
lcd_screen.lcd_display_string("PRESS TO PLAY", 1)
while True:
    time.sleep(0.1)
    if true_button.is_pressed or false_button.is_pressed:
        start_game()
        score = None
        X = Y = Z = None
        correct_answer = None
        update_bool_leds()
        update_score_leds()
        lcd_screen.lcd_display_string("PRESS TO PLAY", 1)
        time.sleep(1)  # Prevent immediate restart

