import logging
import json
import collections
from itertools import dropwhile

logger = logging.getLogger("UIARecorder")


def generate_snippet(generated_path):
    """Генератор кода для запуска

    Args:
        generated_path (dict): Словарь сгенерированными путями

    """
    generated_code = dict()
    if generated_path:
        ordered_path = collections.OrderedDict(
            reversed(sorted(generated_path["path"].items()))
        )

        main_dlg_path = next(iter(ordered_path.values()))
        top_index = int(next(iter(ordered_path.keys())))
        generated_code = (
            "dk.window(class_name='{0}',"
            "control_type='{1}', found_index=0)".format(
                main_dlg_path["class_name"], main_dlg_path["control_type"]
            )
        )

        
        
        for item_path in dropwhile(
            lambda x: int(x[0]) != 0, ordered_path.items()
        ):
            generated_code += (
                ".descendants(class_name='{0}', title='{1}',"
                "control_type='{2}', depth={4})[{3}]".format(
                    item_path[1]["class_name"],
                    item_path[1]["title"],
                    item_path[1]["control_type"],
                    item_path[1]["top_parent_index"],
                    top_index -
                    int(item_path[0]) if int(item_path[0]) > 0 else None,
                )
            )
    return generated_code


def find_element_by_uia(json_path: str, need_print: bool = False) -> dict:
    """[Поиск элемента через pywinauto.Desktop(backend='uia')]

    Args:
        json_path ([str]): [Путь до json файла]
        need_print ([bool]): [False по умолчанию, вывод сгенерированного кода, если True]
    """

    code_inject = """   
from pywinauto import Desktop
dk = Desktop(backend='uia', allow_magic_lookup=False)
    """

    generated_json = get_json_file(json_path)
    generated_code = generate_snippet(generated_json)
    if need_print:
        print(generated_code)
    exec(code_inject)
    elem = eval(generated_code)
    file_name = ' '.join(' '.join(json_path.split('\\')).split('/')).split()[-1]
    logger.info(f"SmartRPA (activity): UIA Element: {file_name}")
    return elem


def get_json_file(filename: str) -> dict:
    """read given json file

    Args:
        filename (str): filename of json file

    Returns:
        dict: json.loads()
    """

    try:
        with open(f'{filename}.json') as outfile:
            return json.load(outfile)
    except FileNotFoundError:
        raise Exception(f'Не найден файл: {filename}')
