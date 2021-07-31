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
    srpa.main_overlay.clear_all()
    srpa.main_overlay.refresh()
    srpa.ss_overlay.clear_all()
    srpa.ss_overlay.refresh()
    srpa.main_overlay.quit()
    srpa.ss_overlay.quit()    
    recorder.stop_thread()
    stop()
    sys.exit()


def on_click(x, y, btn, pressed):
    print(f'{"Pressed" if pressed else "Released"} {btn} at {(x, y)}')
    if pressed and btn.left:
        recorder.get_elem_under_cursor(x, y)
        return False


def on_move(x, y):
    recorder.draw_wrapper_rect_oaam(x, y)


kl = keyboard.GlobalHotKeys({"<ctrl>+<alt>+s": close_recorder})
listener_m = mouse_l(on_move=on_move, on_click=on_click)



def start():
    print("Start...")
    kl.daemon = True
    listener_m.daemon = True
    kl.start()
    listener_m.start()
    return listener_m


def stop():
    print('Stop...')
    kl.stop()
    listener_m.stop()


start()
