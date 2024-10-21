from multiprocessing import Process, Value
import time

def increment(shared_var):
    for _ in range(10):
        time.sleep(1)
        with shared_var.get_lock():  # Защита от состояний гонки
            shared_var.value += 1
            print(f'Incremented: {shared_var.value}')

def decrement(shared_var):
    for _ in range(10):
        time.sleep(1)
        with shared_var.get_lock():  # Защита от состояний гонки
            shared_var.value -= 1
            print(f'Decremented: {shared_var.value}')

if __name__ == '__main__':
    shared_var = Value('i', 0)  # 'i' означает тип integer

    p1 = Process(target=increment, args=(shared_var,))
    p2 = Process(target=decrement, args=(shared_var,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
