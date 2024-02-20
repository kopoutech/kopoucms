import os
import time


def store_modification_time(directory):
    modification_times = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            modification_time = os.path.getmtime(file_path)
            modification_times[file_path] = modification_time
    return modification_times


LAST_CHECKED_TIME = None


def watch_and_render(watch_dir, handler_func, handler_args=[]):
    global LAST_CHECKED_TIME
    if LAST_CHECKED_TIME is None:
        LAST_CHECKED_TIME = time.time()
        handler_func(*handler_args)

    while True:
        try:
            modification_times = store_modification_time(watch_dir)
            for file_path, modification_time in modification_times.items():
                if modification_time > LAST_CHECKED_TIME:
                    print(
                        f"{file_path} was modified at {modification_time} | {LAST_CHECKED_TIME}"
                    )
                    LAST_CHECKED_TIME = time.time()
                    handler_func(*handler_args)
                    break
            time.sleep(2)
        except KeyboardInterrupt:
            print("Exiting...")
            break
        except Exception as e:
            print(e)
            continue

    """
    1701577845.9531233
    1701578510.3865047
    """
