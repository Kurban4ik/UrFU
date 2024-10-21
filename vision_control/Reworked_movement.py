import http
import time
from go import Go

class Catch:
    def __init__(self, go: Go):
        self.go = go
        self.mid = 340
        self.success_point_ball = (1, 1)
        self.success_point_cube = (1, 1)
        self.camera_angle_vied = 108
        self.l_b_ball, self.r_b_ball = 290, 310
        self.l_b_cube, self.r_b_cube = 320, 360

    def catch_box(self):
        while True:
            x, y, X, Y = 0, 0, 0, 0
            try:
                with open('costyl', 'r') as f:
                    x, y, X, Y = list(map(float, f.readline().split()))
            except Exception as e:
                continue
            x_mid = (x + X) // 2
            y_mid = (y + Y) // 2
            last_move = ''
            y_diff = max(0.05, abs(220 - y_mid) * 0.002)
            if y_mid < 200 and 500 > x > 120:
                self.go.fw(y_diff * 2)
                last_move = 'move'
            elif y_mid > 390:
                last_move = 'move'
                self.go.back(y_diff)
            elif not (self.l_b_cube < x_mid < self.r_b_cube):
                self.go.rotate_at_angle((x_mid - self.mid ) * self.camera_angle_vied / 480)
                last_move = 'rotate'
            elif y_mid > 270:
                last_move = 'move'
                self.go.back(y_diff)
            elif y_mid < 235:
                last_move = 'move'
                self.go.fw(y_diff)
            else:
                print(x, y, X, Y)
                print(x_mid, y_mid)
                self.go.catch_box()
                return
            if last_move == 'rotate': time.sleep(0.3)
            else: time.sleep(1)

    def catch_ball(self):
        while True:
            x, y, X, Y = 0, 0, 0, 0
            try:
                with open('costyl', 'r') as f:
                    x, y, X, Y = list(map(float, f.readline().split()))
            except Exception as e:
                continue
            x_mid = (x + X) // 2
            y_mid = (y + Y) // 2
            last_move = ''
            y_diff = max(0.05, abs(220 - y_mid) * 0.002)
            if y_mid < 200 and 500 > x > 120:
                self.go.fw(y_diff * 2)
                last_move = 'move'
            elif y_mid > 390:
                last_move = 'move'
                self.go.back(y_diff)
            elif not (self.l_b_cube < x_mid < self.r_b_cube):
                self.go.rotate_at_angle((x_mid - self.mid) * self.camera_angle_vied / 480)
                last_move = 'rotate'
            elif y_mid > 270:
                last_move = 'move'
                self.go.back(y_diff)
            elif y_mid < 235:
                last_move = 'move'
                self.go.fw(y_diff)
            else:
                print(x, y, X, Y)
                print(x_mid, y_mid)
                self.go.catch_ball()
                return
            if last_move == 'rotate':
                time.sleep(0.3)
            else:
                time.sleep(1)

    def press_button(self):
        pass # В разработке


if __name__ == '__main__':
    go = Go()
    catch = Catch(go)
    catch.catch_ball()