from threading import Thread, Lock
import time
lk = Lock()

def fun():
    for i in range(1, 11):
        lk.acquire()
        print ('Child:', i)
        lk.release()
        time.sleep(1)

if __name__ == '__main__':
    thr1 = Thread(target=fun)

    thr1.start()

    for i in range(10, 21):
        lk.acquire()
        print ('Main: ', i)
        lk.release()
        time.sleep(1)