from time import sleep

from movement_control.move_commands import fw, stop_moving, set_speed, back, left, \
    right

movement_coeff = 0.05
success_pts = list(map(float, '242.524169921875 231.10682678222656 '
                              '361.70269775390625 343.0059814453125'.split()))


def get_mid(dist):
    return int(dist * dist - 56 * dist + 1084)


def count_dist_ball(square):  # возвращает дистанцию до объекта по площади на камере
    return -0.0015701334676403928 * square + 54.02883494683959


def good_speed(dist):
    if dist <= 27:
        return 30
    if dist >= 38:
        return 80
    return 55 * dist / 13 - 1160 * dist / 13


def come_at_distance(d):
    set_speed(good_speed(d))
    time = abs(d * movement_coeff)
    if d > 36:
        time *= 3
    if d > 0:
        fw()
    else:
        back()
    sleep(time)
    stop_moving()


def get_good_delta(dist):
    return 0.07 * dist * dist - 1.4 * dist + 20


def rotate_to_pix(x, mid):
    set_speed(50)
    time = abs(mid - x) / 1700
    if x < mid:
        left()
        sleep(time)
        stop_moving()
    else:
        right()
        sleep(time)
        stop_moving()


def make_a_move_to_ball(x, y, X, Y):
    width = X - x
    height = Y - y
    x_mid = x + width // 2
    right_bound = 36
    left_bound = 30
    dist = count_dist_ball(width * height)
    mid = get_mid(dist)

    print('dist', count_dist_ball(width * height), height * width)
    delta = get_good_delta(dist)
    print('delta', delta)
    if mid - delta > x_mid or x_mid > mid + delta:
        return 'rotate', x_mid, mid
    elif left_bound < dist < right_bound:
        return 'catch',
    else:
        out = dist - (left_bound + right_bound) / 2
        return 'come', out

def make_a_move_to_cube(x, y, X, Y):
    width = X - x
    height = Y - y
    x_mid = x + width // 2
    right_bound = 3
    left_bound = 28
    dist = count_dist_ball(width * height)
    mid = get_mid(dist)
    print(width * height)
    return tuple('1')
if __name__ == '__main__':
    print(get_good_delta(33))
    print(good_speed(40))
