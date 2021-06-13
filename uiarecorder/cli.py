"""Клиент рекордера
"""
import sys
import os

from pynput import mouse, keyboard
from pynput.mouse import Listener as mouse_l
from pynput.keyboard import Listener as keyboard_l
from core import SmartRPAUIElemGetter as srpa


recorder = srpa()


def close_recorder():
    print("Exit")
    srpa.main_overlay.clear_all()
    srpa.main_overlay.refresh()
    srpa.ss_overlay.clear_all()
    srpa.ss_overlay.refresh()
    recorder.stop_thread()
    listener_m.stop()
    sys.exit()


def on_click(x, y, btn, pressed):
    print(f'{"Pressed" if pressed else "Released"} {btn} at {(x, y)}')
    if pressed and btn.left:
        recorder.get_elem_under_cursor(x, y)
    # elif not pressed and btn.left:
    #     recorder.screenshot = recorder.take_buff_screenshot()


def start():
    pass


def on_move(x, y):
    recorder.draw_wrapper_rect_oaam(x, y)




if __name__ == "__main__":
    print("Start...")
    # recorder.show_screenshot_full_screen()

    with keyboard.GlobalHotKeys({"<ctrl>+<alt>+s": close_recorder}) as kl:
        with mouse_l(on_move=on_move, on_click=on_click) as listener_m:
            listener_m.join()
        kl.join()
