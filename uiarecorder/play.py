import json
import collections
from itertools import dropwhile
import pathlib


def generate_snippet(generated_path):
    """Генератор кода для запуска

    Args:
        generated_path (dict): Словарь сгенерированными путями

    """
    result = dict()
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
            lambda x: int(x[0]) > 1 or int(x[0]) == top_index, ordered_path.items()
        ):
            generated_code += (
                ".descendants(class_name='{0}', title='{1}',"
                "control_type='{2}', depth={4})[{3}]".format(
                    item_path[1]["class_name"],
                    item_path[1]["title"],
                    item_path[1]["control_type"],
                    0 if int(item_path[0]) == 0 else item_path[1]["top_parent_index"],
                    top_index - int(item_path[0]) if int(item_path[0]) > 0 else None,
                )
            )
        # result = "elem = {}\nelem.set_focus()\nelem.click_input()".format(generated_code)
        result = generated_code
    return result


def find_element(generated_path):
    """[summary]

    Args:
        generated_path ([type]): [description]
    """
    code_inject = """
from pywinauto import Desktop
dk = Desktop(backend='uia', allow_magic_lookup=False)
    """
    generated_code = generate_snippet(generated_path)
    exec(code_inject)
    print(code_inject)
    print(generated_code)
    elem = eval(generated_code)
    return elem


def get_json_file(filename, elem_dir="recorder_elems"):
    """read given json file

    Args:
        filename (str): filename of json file

    Returns:
        dict: json to dict
    """

    result = dict()

    if not filename:
        print("Filename is required!")
        return

    current_dir = pathlib.Path(__file__).parents[1]
    elem_dir_ = pathlib.Path.joinpath(current_dir, elem_dir)

    if not pathlib.Path(elem_dir_).is_dir():
        print(f'Directory "{elem_dir}" does not exist!')
        return
    elem_file = pathlib.Path.joinpath(current_dir, elem_dir, f"{filename}.json")

    if not pathlib.Path.is_file(elem_file):
        print(f"Please, pass the correct filename. File does not exist: {filename}")
        return

    with open(elem_file) as outfile:
        result = json.load(outfile)

    return result


# path = get_json_file('elem_9x84mand')
# elem = find_element(path)
# elem.set_focus()

path = get_json_file("elem_79apaet7")
elem = find_element(path)
# elem.set_focus()
elem.draw_outline()
