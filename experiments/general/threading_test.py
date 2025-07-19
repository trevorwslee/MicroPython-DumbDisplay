import time, _thread



RunningCountLock = None
RunningCount = 0

def print_time(thread_name, delay):
    global RunningCount
    try:
        RunningCountLock.acquire()
        RunningCount += 1
    finally:
        RunningCountLock.release()
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print(f'RunningCount={RunningCount} ... thread_name={thread_name} ... time:{time.localtime()}')
    try:
        RunningCountLock.acquire()
        RunningCount -= 1
    finally:
        RunningCountLock.release()
        print(f'Exited ... thread_name={thread_name}')


if __name__ == "__main__":

    RunningCountLock = _thread.allocate_lock()

    try:
        _thread.start_new_thread(print_time, ('Thread-1', 1, ))
        time.sleep(1.5)
        _thread.start_new_thread(print_time, ('Thread-2', 1, ))
    except:
        print('Error: unable to start thread')

    while True:
        time.sleep(0.5)
        print("...")
        try:
            RunningCountLock.acquire()
            if RunningCount == 0:
                break
        finally:
            RunningCountLock.release()

    print("***** ALL DONE *****")