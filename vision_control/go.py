import time
import socket

def num_to_time_bytes(num):
    num = int(num)
    num = bin(num)[2:]
    marc = len(num) - 1
    res1 = ''
    res2 = ''
    for i in range(8):
        if marc >= 0:
            res1 += num[marc]
        else:
            res1 += '0'

        marc -= 1
    for i in range(8):
        if marc >= 0:
            res2 += num[marc]
        else:
            res2 += '0'
        marc -= 1
    res1, res2 = res1[::-1], res2[::-1]
    return int(res2, 2).to_bytes(1, byteorder='big') + int(res1, 2).to_bytes(1, byteorder='big')


class Go:
    def __init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect(('192.168.2.35', 2001))
        self.lights = 0
        self.connection.sendall(b'\xff\x40\x09\x00\xff')  # Выключаем фары
    def mega_slow(self):
        self.set_speed(15)

    def slow(self):
        self.set_speed(30)

    def reg_speed(self):
        self.set_speed(50)

    def fast(self):
        self.set_speed(80)

    def set_speed(self, speed):
        speed = int(speed)
        speed = (b'\xFF\x02\x01' + speed.to_bytes(1, byteorder='big') + b'\xFF' +
                 b'\xFF\x02\x02' + speed.to_bytes(1, byteorder='big') + b'\xFF')
        self.connection.sendall(speed)

    def fw(self, t):
        t *= 1000
        self.connection.sendall(b'\xff\xfd' + num_to_time_bytes(t) + b'\xff')
        time.sleep(t / 1000)

    def back(self, t):
        t *= 1000
        self.connection.sendall(b'\xff\xf4' + num_to_time_bytes(t) + b'\xff')
        time.sleep(t / 1000)

    def left(self, t):
        t *= 1000
        self.connection.sendall(b'\xff\xf5' + num_to_time_bytes(t) + b'\xff')
        time.sleep(t / 1000)

    def right(self, t):
        t *= 1000
        self.connection.sendall(b'\xff\xf6' + num_to_time_bytes(t) + b'\xff')
        time.sleep(t / 1000)

    def rotate_at_angle(self, angle):
        self.reg_speed()
        rotate_time = max(0.01, abs(angle * 480 / (3400 * 108)))
        if angle > 0:
            self.right(rotate_time)
        else:
            self.left(rotate_time)
        time.sleep(rotate_time)

    def stop(self):
        self.connection.sendall(b'\xff\x00\x00\x00\xff')

    def set_servo_angle(self, angle, num):
        self.connection.sendall(b'\xFF\x01' + int(num).to_bytes(1, byteorder='big') +
                                int(angle).to_bytes(1, byteorder='big')
                                + b'\xFF')
        time.sleep(1)

    def normal(self):  # ТРЕБУЕТ ВРЕМЯ ########################
        positions = ((75, 7), (20, 8), (60, 4), (80, 4), (50, 3), (180, 2), (160, 1))
        for i in positions:
            self.set_servo_angle(*i)

    def straight_servo(self):
        positions = ((93, 3), (150, 2), (93, 1), (180, 2), (87, 1))
        for i in positions:
            self.set_servo_angle(*i)

    def lights(self):
        if self.lights:
            self.connection.sendall(b'\xff\x40\x09\x00\xff')
            self.lights = 0
        else:
            self.connection.sendall(b'\xff\x40\x09\x08\xff')
            self.lights = 1

    def prepare_to_catch(self):
        self.set_servo_angle(93, 3)
        self.set_servo_angle(55, 4)

    def catch_ball(self):
        self.slow()
        self.fw(0.2)
        self.prepare_to_catch()
        self.straight_servo()
        self.fw(0.1)
        time.sleep(0.6)
        self.set_servo_angle(84, 4)
        self.up()
        self.reg_speed()

    def catch_box(self):
        self.slow()
        self.fw(0.2)
        self.prepare_to_catch()
        self.straight_servo()
        self.fw(0.6)
        time.sleep(0.3)
        self.set_servo_angle(75, 4)
        self.up()
        self.reg_speed()
    def up(self):
        for j in range(120, 180, 20):
            self.set_servo_angle(j, 1)
        self.set_servo_angle(120, 2)

    def put_on_floor(self):
        self.set_servo_angle(120, 1)
        self.set_servo_angle(55, 4)

    def put_in_basket(self):
        self.set_servo_angle(55, 4)