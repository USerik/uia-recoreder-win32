"""Клиент рекордера
"""
import sys
import os

from pynput import mouse, keyboard
from pynput.mouse import Listener as mouse_l
from pynput.keyboard import Listener as keyboard_l
from .core import SmartRPAUIElemGetter as srpa


recorder = srpa()

def close_recorder():
    print("Exit")
    listener_m.stop()
    srpa.main_overlay.clear_all()
    srpa.main_overlay.refresh()
    srpa.ss_overlay.clear_all()
    srpa.ss_overlay.refresh()
    recorder.stop_thread()
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

listener_m = mouse_l(on_move=on_move, on_click=on_click)

def start():
    listener_m.start()
    print("Start...")
    with keyboard.GlobalHotKeys({"<ctrl>+<alt>+s": close_recorder}) as kl:        
        kl.join()
