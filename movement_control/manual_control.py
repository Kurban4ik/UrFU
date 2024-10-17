import keyboard  # using module keyboard
import socket

from connection import send_command, create_connection, close_connection
from move_commands import set_speed, fw, left, back, right, stop_moving, scenario1, put, normal, connect, host, port, catch, up

set_speed(40)

active = 'l'

iterr = 0
while True:  # making a loop
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('a'):  # if key 'q' is pressed
            if active != 'l':
                left()
            active = 'l'
        elif keyboard.is_pressed('d'):  # if key 'q' is pressed
            if active != 'r':
                right()
            active = 'r'
        elif keyboard.is_pressed('w'):  # if key 'q' is pressed
            if active != 'w':
                fw()
            active = 'w'
        elif keyboard.is_pressed('s'):  # if key 'q' is pressed
            if active == 's':
                back()
            active = 's'
        elif keyboard.is_pressed('h'):
            scenario1()
        elif keyboard.is_pressed('j'):
            put()
        elif keyboard.is_pressed('n'):
            normal()
        elif keyboard.is_pressed('c'):
            catch()
            up()
        else:
            if active != ' ':
                stop_moving()
            active = ' '
    except:
        break  # if user pressed a key other than the given key the loop will break
