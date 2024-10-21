from vision_control.Reworked_movement import Go, Catch
from vision_control.reworked_vision import NewView
from multiprocessing import Process, Value

if __name__ == '__main__':

    go = Go()

    shared_var = Value('i', 0)  # 'i' означает тип integer
    catch = Catch(go, shared_var)
    view = NewView(shared_var)

    p1 = Process(target=catch.catch_ball, args=())
    p2 = Process(target=view.view, args=())
    p2.run()
    p1.start()