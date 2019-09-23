# Rotary Encoder 07/30/2018
# TSWB 7 function Tact and Scroll Wheel
#   
# Rating:  1 ma , 10 VDC 
# Determines position change +/- 1 for use to move mouse

import time
import board
import digitalio
import rotaryio

class Button():
    def __init__(self, pin, _active_value):
        self.button = digitalio.DigitalInOut(pin)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.UP
        self.active_value = _active_value
        self.state = 'NOT_PRESSED'        
        
    def update(self):
        just_pressed = False
        if self.button.value == self.active_value and self.state == 'NOT_PRESSED':
            self.state = 'PRESSED'
            just_pressed = True
        elif self.button.value != self.active_value and self.state == 'PRESSED':  
            self.state = 'NOT_PRESSED'   
        else:
            pass
        return just_pressed    
        
# LED 
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT
led.value = False

# RotaryIO , using pins D10 , D9
encoder = rotaryio.IncrementalEncoder(board.D10, board.D9)

# Rotary Encoder Module buttons 
# Pins board.D11 , board.D12
x_rot_button = Button(board.D11,0)
y_rot_button = Button(board.D12,0)


position_change = 0
last_position = encoder.position

while True:
    led.value = False  
  
    if x_rot_button.update():
        print('X_ROT Pressed') 
    if y_rot_button.update():
        print('Y_ROT Pressed')  
        
    position = encoder.position
    if position != last_position:
        position_change = position - last_position
        print(position_change)        
        last_position = position
        
    led.value = True    