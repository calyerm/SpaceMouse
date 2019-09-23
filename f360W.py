# Fusion 360 3D Control 07/31/2018
# Rotate Control
#   Rotate X
#       1. Press KBD shift
#       2. Press middle mouse button
#       3. Move mouse along X axis
#   Rotate Y
#       1. Press KBD shift
#       2. Press middle mouse button
#       3. Move mouse along y axis
#
# Notes:
#  Neopixel:
#   Power 3.3 V , Connected to pin 8 , CircuitPython pin name is board.NEOPIXEL
import time
import board
import digitalio
import rotaryio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
import neopixel

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

# Neopixel RGB LED
RGB_BLUE = (0,255,0)
RGB_GREEN = (0,0,255)
RGB_OFF   = (0,0,0)
rgb_led = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=.3)
def rgb_led_display(color):
    rgb_led[0] = color
    rgb_led.show()

# RotaryIO , using pins D10 , D9
encoder = rotaryio.IncrementalEncoder(board.D10, board.D9)       

last_position = encoder.position
def rot_encode():
    global last_position   
    position = encoder.position   
    position_change = 0       
    if position != last_position:
        position_change = position - last_position
        #print(position_change)        
        last_position = position   
        #print(position_change) 
    return position_change
       
# Rotary Encoder Module buttons , using pins board.D11 , board.D12
x_rot_button = Button(board.D11,0)
y_rot_button = Button(board.D12,0)  


def rot_buttons():   
    axis = None
    if x_rot_button.update():
        axis = 'x'
        rgb_led_display(RGB_GREEN)  
    if y_rot_button.update():
        axis = 'y'
        rgb_led_display(RGB_BLUE)    
    return axis

# Keyboard
kbd = Keyboard()

# Mouse
mouse = Mouse()

rot_ctrl_state = 'DISABLED'
rot_axis = None
def rot_ctrl():
    global rot_ctrl_state   
    global rot_axis  
    global last_position   
    axis = rot_buttons()
    if axis is not None and rot_ctrl_state == 'DISABLED':
        # press SHIFT KEY
        kbd.press(Keycode.LEFT_SHIFT) 
        time.sleep(0.02)         
        # press MIDDLE Mouse button       
        mouse.press(Mouse.MIDDLE_BUTTON)
        time.sleep(0.02)   
        rot_ctrl_state = 'ENABLED'
        rot_axis = axis
        last_position = encoder.position        
        #print('Enable')          
    elif axis is not None and rot_ctrl_state == 'ENABLED':
        # Release all keys        
        kbd.release_all()
        mouse.release_all()         
        rot_ctrl_state = 'DISABLED' 
        rot_axis = None         
        rgb_led_display(RGB_OFF)      
        time.sleep(0.02) 
        #print('Disable')        
    else:
        pass
    return rot_ctrl_state,rot_axis
 
def mouse_ctrl(axis , pc): 
    if pc == 0 or axis is None:
       return        
    _x = 0
    _y = 0   
    _d = 1
    if pc < 0:
        _d = -1   
    # Rotary control clockwise mouse moves to right     
    if 'x' == axis:
        _x = _d
    # Rotary control clockwise mouse moves to up        
    if 'y' == axis:
        _y = -_d   
        
    for _ in range(abs(pc)):
        led.value = True   
        time.sleep(0.02)      
        mouse.move(_x,_y,0) 
        led.value = False   
        
rgb_led_display(RGB_OFF) 
while True:   
    
    # Response delay   
    time.sleep(0.1)
    
    # Process rotation enable/disable    
    rot_enable , rot_axis = rot_ctrl()   
   
    if 'DISABLED' == rot_enable:
        continue     
    
    # If rotary encoder change , move mouse   
    rot_inc = rot_encode()   
    mouse_ctrl(rot_axis,rot_inc)
    
   
   