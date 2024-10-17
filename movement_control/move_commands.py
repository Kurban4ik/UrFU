import time
from sys import byteorder

from connection import create_connection, send_command, host, port

forward = b'\xFF\x00\x01\x00\xFF'
stop = b'\xFF\x00\x00\x00\xFF'
turn_left = b'\xFF\x00\x03\x00\xFF'
turn_right = b'\xFF\x00\x04\x00\xFF'
reverse = b'\xFF\x00\x02\x00\xFF'
connect = create_connection(host, port)


def set_speed(speed):
    setfullspeed = (b'\xFF\x02\x01' + speed.to_bytes(1, byteorder='big') + b'\xFF' +
                    b'\xFF\x02\x02' + speed.to_bytes(1, byteorder='big') + b'\xFF')
    send_command(connect, setfullspeed)

def fw():
    send_command(connect, forward)

def stop_moving():
    send_command(connect, stop)

def back():
    send_command(connect, reverse)


def left():
    send_command(connect, turn_left)


def right():
    send_command(connect, turn_right)

def set_servo_angle(angle, num):
    send_command(connect, b'\xFF\x01' + int(num).to_bytes(1, byteorder='big') +
                 int(angle).to_bytes(1, byteorder='big')
                 + b'\xFF')
    time.sleep(0.5)

def normal():
    set_servo_angle(20, 8)
    set_servo_angle(80, 7)
    set_servo_angle(60, 4)
    set_servo_angle(80, 4)
    set_servo_angle(50, 3)
    set_servo_angle(180, 2)
    set_servo_angle(160, 1)


def straight_servo():
    set_servo_angle(93, 3)
    set_servo_angle(180 , 2)
    set_servo_angle(86, 1)


def prepare_to_catch():
    set_servo_angle(93, 3)
    set_servo_angle(50, 4)

def catch():
    set_servo_angle(85, 1)
    set_servo_angle(87, 4)

def up():
    for j in range(120, 180, 20):
        set_servo_angle(j, 1)
    set_servo_angle(120, 2)

def put():
    set_servo_angle(55, 4)

def scenario1():
    prepare_to_catch()
    straight_servo()

if __name__ == '__main__':
    set_servo_angle(160, 1)