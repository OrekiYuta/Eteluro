import os
from datetime import datetime
import logging
import pyautogui
import pynput.mouse
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
import multiprocessing

PATH_RECORD_SCREEN = "./record_screen/"
PATH_RECORD_KEYBOARD_MOUSE = "./record_keyboard_mouse/"
PATH_RECORD_SCREEN = "/record_screen/"
FILE_DATE_FORMAT = datetime.now().strftime('%Y-%m-%d')


def on_press(key):
    key_msg = "Key pressed: {0}".format(key)


def on_release(key):
    key_msg = "Key released: {0}".format(key)

    key_msg_cn = "键盘按下: {0} 键位".format(key)

    keyboard_log = kb_log()
    keyboard_log.info(key_msg_cn)

    print(key_msg_cn)
    print("当前主进程", os.getpid(), os.getppid())
    multi_process_creator()


def on_move(x, y):
    ms_msg = "Mouse moved to ({0}, {1})".format(x, y)


def on_click(x, y, button, pressed):
    button_point = ""
    if button == pynput.mouse.Button.left:
        button_point = "左键"
    if button == pynput.mouse.Button.middle:
        button_point = "中键"
    if button == pynput.mouse.Button.right:
        button_point = "右键"

    if pressed:
        ms_msg = 'Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button)
    else:
        ms_msg = 'Mouse released at ({0}, {1}) with {2}'.format(x, y, button)
        ms_msg_cn = '鼠标移动到了 ({0}, {1}) 坐标位置, 并使用鼠标 {2} 点击'.format(x, y, button_point)

        mouse_log = ms_log()
        mouse_log.info(ms_msg_cn)

        print(ms_msg_cn)
        print("当前主进程", os.getpid(), os.getppid())
        # TODO 这里可以做个坐标判断处理，如果还是同样的坐标的话，就不执行下面的截图操作，防止鼠标瞬间多次点击造成卡顿循环
        multi_process_creator()


def on_scroll(x, y, dx, dy):
    ms_msg = 'Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy)


def kb_log():
    file_name = "/keyboard-" + FILE_DATE_FORMAT + ".txt"
    full_path = PATH_RECORD_KEYBOARD_MOUSE + file_name

    key_logger = get_logger('KeyBoardHandler', full_path, logging.INFO)
    return key_logger


def ms_log():
    file_name = "/mouse-" + FILE_DATE_FORMAT + ".txt"
    full_path = PATH_RECORD_KEYBOARD_MOUSE + file_name

    mouse_logger = get_logger('MouseBoardHandler', full_path, logging.INFO)
    return mouse_logger


def get_logger(logger_name, logger_path, logger_level):
    # log_format = "%(asctime)s - %(levelname)s - %(message)s"
    log_format = "%(asctime)s - %(message)s"
    # log_format = "%(asctime)s.%(msecs)03d- %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S %p"

    keyboard_mouse_daily_save_path = os.getcwd() + PATH_RECORD_KEYBOARD_MOUSE
    path_creator(keyboard_mouse_daily_save_path)

    formatter = logging.Formatter(log_format, date_format)
    file_handler = logging.FileHandler(logger_path, mode='a', encoding='utf-8')
    file_handler.setFormatter(formatter)

    obj_log = logging.getLogger(logger_name)

    # 如果已经实例过一个相同名字的 logger，则不用再追加 handler
    if not obj_log.handlers:
        obj_log.setLevel(logger_level)
        obj_log.addHandler(file_handler)

    return obj_log


def screenshot():
    day_date = datetime.now().strftime('%Y-%m-%d')
    screen_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    full_path = PATH_RECORD_SCREEN + day_date + "/" + screen_time + ".png"

    print("当前子进程", os.getpid(), os.getppid())
    print('----------------------------------------------')

    try:
        current_screen = pyautogui.screenshot()
        print("当前画面", current_screen)

        screen_save_path = os.getcwd() + PATH_RECORD_SCREEN
        path_creator(screen_save_path)
        screen_daily_save_path = os.getcwd() + PATH_RECORD_SCREEN + "\\" + day_date
        path_creator(screen_daily_save_path)

        current_screen.save("." + full_path)
    except:
        print("异常发生，无法获取当前画面，可能是锁屏或者远程桌面退出")
        pass


def multi_process_creator():
    process = multiprocessing.Process(target=screenshot)
    process.start()


def path_creator(full_path):
    if not os.path.exists(full_path):
        os.mkdir(full_path)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    # Set up the listener threads
    keyboard_listener = KeyboardListener(on_press=on_press, on_release=on_release)
    mouse_listener = MouseListener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)

    # Start the threads and join them so the script doesn't end early
    keyboard_listener.start()
    mouse_listener.start()

    keyboard_listener.join()
    mouse_listener.join()
