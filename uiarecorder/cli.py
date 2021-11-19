"""Клиент рекордера
"""
import sys
import os
import logging

from pynput import mouse, keyboard
from pynput.mouse import Listener as mouse_l
from pynput.keyboard import Listener as keyboard_l
from .core import SmartRPAUIElemGetter as srpa

logger = logging.getLogger("Robot")
recorder = srpa()
mouse_c = mouse.Controller()

def close_recorder():
    print("Exit")
    try:
        srpa.main_overlay.clear_all()
        srpa.main_overlay.refresh()
        srpa.ss_overlay.clear_all()
        srpa.ss_overlay.refresh()
        srpa.main_overlay.quit()
        srpa.ss_overlay.quit()
        recorder.stop_thread()
    except:
        pass
    finally:
        stop()
        sys.exit()


def on_click(x, y, btn, pressed):
    logger.info(f'{"Pressed" if pressed else "Released"} {btn} at {(x, y)}')
    if pressed and btn.left:
        recorder.get_elem_under_cursor(x, y)
        return False


def on_move(x, y):
    recorder.draw_wrapper_rect_oaam(x, y)

def get_elem_capture():
    x, y = mouse_c.position
    recorder.get_elem_under_cursor(x, y)

kl = keyboard.GlobalHotKeys({"<ctrl>+<alt>+s": close_recorder, "<ctrl>+<shift>+f": get_elem_capture})
listener_m = mouse_l(on_move=on_move)


def start():
    logger.info("Start...")
    # kl.daemon = True
    # listener_m.daemon = True
    kl.start()
    listener_m.start()


def stop():
    logger.info('Stop...')
    kl.join()
    listener_m.join()
    kl.stop()
    listener_m.stop()
