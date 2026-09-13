import time
import sys

def delay_print(s):
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(.05)

def loading_city_animation(city_name, function):
    import threading
    import time

    stop = threading.Event()
    message = f"Getting weather for {city_name}"

    def animate():
        dots = ["   ", ".  ", ".. ", "..."]
        i = 0

        while not stop.is_set():
            print(f"\r{message}{dots[i]}", end="", flush=True)
            time.sleep(0.3)
            i = (i + 1) % 4

    thread = threading.Thread(target=animate)
    thread.start()

    try:
        result = function()
    finally:
        stop.set()
        thread.join()

    print("\r" + message + "   ")
    return result