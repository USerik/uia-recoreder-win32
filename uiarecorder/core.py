# -*- coding: utf-8 -*-

"""
Автор: Уатханов С.
email: seriku2@halykbank.kz

Модуль запись действия пользователя
"""


from datetime import time
import os
import queue
import threading
import traceback
import collections
import json
import base64
import tempfile
import warnings
import time
import pywintypes

import tkinter as tk
from tkinter import simpledialog

from io import BytesIO
from queue import Queue
from itertools import dropwhile

import unicodedata
import re

from pathlib import Path
import PIL
import pywinauto

import comtypes
import win32api
import win32gui
from win32con import WM_COMMAND
from win32gui import FindWindow, SendMessage


from PIL import ImageGrab


import overlay_arrows_and_more as oaam

warnings.simplefilter("ignore", UserWarning)


class SmartRPAUIElemGetter:
    """[summary]

    Returns:
        [type]: [description]
    """

    queue = Queue()
    previous_wrapper = None
    previous_wrapper_rect = None
    recorder_elems_path = str(Path(Path.cwd()).joinpath("recorder_elems"))
    main_overlay = oaam.Overlay()
    ss_overlay = oaam.Overlay()

    temp_dir = f"{os.path.split(__file__)[0]}/temp"

    def __init__(self, elems_path=""):
        self.desktop_obj = pywinauto.Desktop(
            backend="uia", allow_magic_lookup=False)
        self.screenshot = self.take_buff_screenshot()

        if os.environ.get("RECORDER_ELEMS_PATH") is not None:
            self.recorder_elems_path = os.environ.get("RECORDER_ELEMS_PATH")
        elif elems_path != "":
            self.recorder_elems_path = elems_path
        else:
            self.recorder_elems_path = str(
                Path(Path.cwd()).joinpath("recorder_elems"))

        self.thread_is_alive = True
        self.thread = threading.Thread(target=self.worker)
        self.thread.start()

        self.create_temp_folder()

    def stop_thread(self):
        self.thread_is_alive = False
        self.thread.join()

    @classmethod
    def minimize_all_windows(cls):
        """Minimize all windows WinOS"""

        hwnd = FindWindow("Shell_TrayWnd", None)
        SendMessage(hwnd, WM_COMMAND, 419, 0)

    def save_into_json(self, data):
        """[summary]

        Args:
            date ([type]): [description]
        """
        Path(self.recorder_elems_path).mkdir(exist_ok=True)
        filename = ".".join([self.user_input_gui(), 'json'])
        if filename:
            with open(Path(self.recorder_elems_path).joinpath(filename), 'w', encoding='utf-8') as outfile:
                json.dump(obj=data, fp=outfile, indent=4, sort_keys=True)
        else:
            with tempfile.NamedTemporaryFile(
                mode="w",
                prefix="elem_",
                suffix=".json",
                delete=False,
                dir=self.recorder_elems_path,
            ) as outfile:
                json.dump(obj=data, fp=outfile, indent=4, sort_keys=True)

    def worker(self):
        """Обработка событии в очереди"""
        while True:
            if not self.thread_is_alive:
                break
            try:
                task = self.queue.get(timeout=3)
            except queue.Empty:
                continue
            wrapper = task["wrapper"]
            elem_image = self.get_elem_image(wrapper)
            elem_rect = wrapper.rectangle()
            elem_path = self.get_element_path(wrapper)
            self.queue.task_done()
            json_data = {
                "image": elem_image,
                "rect": {
                    "L": elem_rect.left,
                    "T": elem_rect.top,
                    "R": elem_rect.right,
                    "B": elem_rect.bottom,
                },
                "mouse_coords": {"x": task["x"], "y": task["y"]},
                "path": elem_path,
            }
            self.draw_wrapper_rect_oaam(task["x"], task["y"], (0, 255, 0))
            self.save_into_json(json_data)

    @classmethod
    def refresh_screen(cls):
        """
        docstring
        """

        hwnd = win32gui.WindowFromPoint((0, 0))
        monitor = (0, 0, win32api.GetSystemMetrics(
            0), win32api.GetSystemMetrics(1))
        win32gui.InvalidateRect(hwnd, monitor, True)

    def is_same_wrapper(self, x_coordinates, y_coordinates) -> bool:
        result = True
        try:
            rect = self.get_elem_rect(x_coordinates, y_coordinates)
            if rect != self.previous_wrapper_rect:
                self.previous_wrapper_rect = rect
                result = False
        except comtypes.COMError:
            return result

        return result

    def draw_wrapper_rect_oaam(self, x, y, rgb_tuple=(255, 0, 0)):
        rect = self.get_elem_rect(x, y)
        if self.previous_wrapper_rect != rect:
            self.main_overlay.clear_all()
            self.previous_wrapper_rect = rect
            self.main_overlay.add(
                geometry=oaam.Shape.rectangle,
                x=rect.left - 5,
                y=rect.top - 5,
                width=rect.width() + 10,
                height=rect.height() + 10,
                thickness=3,
                color=rgb_tuple,
            )
            try:
                self.main_overlay.refresh()
            except pywintypes.error:
                pass
            
        elif rgb_tuple != (255, 0, 0):
            self.main_overlay.clear_all()
            self.previous_wrapper_rect = rect
            self.main_overlay.add(
                geometry=oaam.Shape.rectangle,
                x=rect.left,
                y=rect.top,
                width=rect.width(),
                height=rect.height(),
                thickness=3,
                color=rgb_tuple,
            )
            self.main_overlay.refresh()

    def draw_red_outline(self, x_coordinates, y_coordinates):
        """
        docstring
        """
        try:
            wrapper = self.desktop_obj.from_point(x_coordinates, y_coordinates)
        except comtypes.COMError:
            return

        if wrapper != self.previous_wrapper:
            self.refresh_screen()
            self.previous_wrapper = wrapper
            wrapper.draw_outline(colour="red", thickness=3)

        if not self.previous_wrapper:
            self.refresh_screen()
            wrapper.draw_outline(colour="red", thickness=3)

    def get_elem_rect(self, x_coordinates, y_coordinates):
        """[summary]

        Args:
            x_coordinates ([type]): [description]
            y_coordinates ([type]): [description]
        """
        try:
            wrapper = self.desktop_obj.from_point(x_coordinates, y_coordinates)
        except comtypes.COMError:
            return None

        return wrapper.rectangle()

    def get_elem_under_cursor(self, x_coordinates, y_coordinates):
        """Метод получения wrapper расположенный под курсором

        Args:
            x_coordinates (int): x координаты мыши
            y_coordinates (int): y координаты мыши

        Returns:
            wrapper: возвращает pywinauto UIAWrapper
        """
        wrapper = self.desktop_obj.from_point(x_coordinates, y_coordinates)
        self.queue.put(
            {"wrapper": wrapper, "x": x_coordinates, "y": y_coordinates})

        return wrapper

    def get_elem_image(self, wrapper):
        """Метод получения картинки элемента

        Args:
            wrapper: объект pywinauto uiawrapper

        Returns:
            base64: картинка или False
        """
        result = None
        elem_image = None

        if wrapper:
            # elem_image = wrapper.capture_as_image()

            try:
                w, h = PIL.Image.open(self.screenshot).size
                rect = wrapper.rectangle()
                elem_image = PIL.Image.open(self.screenshot).crop(
                    (int(rect.left), int(rect.top), int(
                        rect.right), int(rect.bottom))
                )
            except Exception as err:
                # TODO must be logged
                print(err)
                traceback.print_exc()

        if elem_image:
            buff = BytesIO()
            elem_image.save(buff, format="PNG")
            result = base64.b64encode(buff.getvalue()).decode("utf-8")

        return result

    @classmethod
    def get_element_path(cls, wrapper):
        """Генератор пути до элемента

        Args:
            wrapper (pywinauto UIAWrapper): элемент pywinauto

        Returns:
            dict(): возвращает словарь элементов
        """
        try:
            top_parent = wrapper.top_level_parent()
            gen_path = {}
            i = 0

            def top_parent_index(wrapper):
                ctrl_index = 0
                try:
                    ctrl_index = wrapper.top_level_parent().descendants(
                        title=wrapper.window_text(),
                        class_name=wrapper.element_info.class_name,
                        control_type=wrapper.element_info.control_type,
                    ).index(wrapper)
                except ValueError:
                    ctrl_index = 0
                return ctrl_index

            def parent_index(wrapper):
                ctrl_index = 0
                try:
                    ctrl_index = (
                        wrapper.parent()
                        .descendants(
                            title=wrapper.window_text(),
                            class_name=wrapper.element_info.class_name,
                            control_type=wrapper.element_info.control_type,
                        )
                        .index(wrapper)
                    )
                except ValueError:
                    ctrl_index = 0
                return ctrl_index

            while wrapper != top_parent:
                gen_path[i] = {
                    "class_name": wrapper.element_info.class_name,
                    "title": wrapper.window_text().replace("\r", ""),
                    "control_type": wrapper.element_info.control_type,
                    "parent_index": parent_index(wrapper),
                    "top_parent_index": top_parent_index(wrapper),
                    "handle": wrapper.element_info.handle,
                    "automation_id": wrapper.element_info.automation_id,
                }
                #    "depth": i}
                wrapper = wrapper.parent()

                if not wrapper:
                    break

                i += 1

            gen_path[i] = {
                "class_name": top_parent.element_info.class_name,
                "title": top_parent.window_text(),
                "control_type": top_parent.element_info.control_type,
            }

        except ValueError:
            # TODO must be logged
            traceback.print_exc()
            return {}
        except AttributeError:
            # TODO must be logged
            traceback.print_exc()
            return {}
        except Exception as err:
            # TODO must be logged
            print(f"Woops\n {err}")
            traceback.print_exc()
            return {}
        return gen_path

    @classmethod
    def generate_code_from_path_descendants(cls, generated_path):
        """Генератор кода для запуска

        Args:
            generated_path (dict): Словарь сгенерированными путями

        """
        result = dict()
        if generated_path:
            ordered_path = collections.OrderedDict(
                reversed(sorted(generated_path.items()))
            )

            main_dlg_path = next(iter(ordered_path.values()))
            top_index = next(iter(ordered_path.keys()))
            generated_code = (
                "dk.window(class_name='{0}',"
                "control_type='{1}', found_index=0)".format(
                    main_dlg_path["class_name"], main_dlg_path["control_type"]
                )
            )

            for item_path in dropwhile(
                lambda x: x[0] > 1 or x[0] == top_index, ordered_path.items()
            ):
                generated_code += (
                    ".descendants(class_name='{0}', title='{1}',"
                    "control_type='{2}', depth={4})[{3}]".format(
                        item_path[1]["class_name"],
                        item_path[1]["title"],
                        item_path[1]["control_type"],
                        0 if item_path[0] == 0 else item_path[1]["top_parent_index"],
                        top_index - item_path[0] if item_path[0] > 0 else None,
                    )
                )
            result = "elem = {}\nelem.set_focus()\nelem.click_input()".format(
                generated_code
            )
        return result

    def take_buff_screenshot(self):
        buff = BytesIO()
        img = ImageGrab.grab(all_screens=True)
        img.save(buff, format="png")
        return buff

    @classmethod
    def detect_left_top_coner(cls):
        pass

    @classmethod
    def save_temp_screenshot(cls, img: PIL.Image.Image) -> str:
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".png") as png:
            png.write(img)
            return png.name

    def create_temp_folder(self):
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

    def show_screenshot_full_screen(self):
        self.ss_overlay.clear_all()
        self.main_overlay.clear_all()
        self.main_overlay.refresh()
        self.ss_overlay.refresh()
        time.sleep(3)

        self.screenshot = self.take_buff_screenshot()
        # with tempfile.NamedTemporaryFile(
        #         mode="wb",
        #         suffix='.png',
        #         dir=self.temp_dir) as temp_png:
        #     temp_png.write(temp_img.getvalue())
        size_x, size_y = PIL.Image.open(self.screenshot).size
        img = oaam.load_buff_png(self.screenshot.getvalue(), size_x, size_y)
        # img = oaam.load_ico('test.bmp', 3840, 1080)
        self.ss_overlay.add(geometry=oaam.Shape.image, hicon=img, x=0, y=0)
        self.ss_overlay.refresh()

    def user_input_gui(self) -> str:
        ROOT = tk.Tk()
        ROOT.withdraw()
        while True:
            user_input = self.slugify(simpledialog.askstring(
                title="Название элемента", prompt="Введите название элемента:"))
            if user_input:
                break
        return user_input

    @classmethod
    def slugify(cls, value, allow_unicode=False):
        """
        Taken from https://github.com/django/django/blob/master/django/utils/text.py
        Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
        dashes to single dashes. Remove characters that aren't alphanumerics,
        underscores, or hyphens. Convert to lowercase. Also strip leading and
        trailing whitespace, dashes, and underscores.
        """
        value = str(value)
        if allow_unicode:
            value = unicodedata.normalize('NFKC', value)
        else:
            value = unicodedata.normalize('NFKD', value).encode(
                'ascii', 'ignore').decode('ascii')
        value = re.sub(r'[^\w\s-]', '', value.lower())
        return re.sub(r'[-\s]+', '-', value).strip('-_')
