# import json

# # my_dict = {0: {'class_name': '', 'title': 'Проводник', 'control_type': 'Button', 'parent_index': 0, 'top_parent_index': 0, 'handle': None, 'automation_id': 'Microsoft.Windows.Explorer'}, 1: {'class_name': 'MSTaskListWClass',
# #                                                                                                                                                                                                'title': 'Работающие приложения', 'control_type': 'ToolBar', 'parent_index': 0, 'top_parent_index': 0, 'handle': 65804, 'automation_id': ''}, 2: {'class_name': 'Shell_TrayWnd', 'title': 'Панель задач', 'control_type': 'Pane'}}
# # with open("sample.json", "w") as outfile:
# #     json.dump(obj=my_dict, fp=outfile, indent=4, sort_keys=True)

# with open("sample.json", "r") as file:
#     print(json.load(file))


import base64
image_data_ = b"iVBORw0KGgoAAAANSUhEUgAAASgAAAAWCAIAAAD8YpYnAAAEbklEQVR4nO2bT2jiaBjGny578d5hQYQVXMoIodCLQWFpYBcseygGB0ph5qJzEESS7kHKQimlUIqHVQmFPYy9zGEQRpQehgpdiCzUjZdCCTjsbqClYaDMnDfXPZjERBNbHTWz7fc75c/75fn43rz6vIkulP78F9NmYWFh6tckEB4SX3k9AQLhMUIKj0DwAFJ4BIIHkMIjEDyAFB6B4AFfz0tIEdNUXQYAUIWdSm5xXsIE7xhM+sdD3291W0SQL/hL+XNjN1bSNqIAmlX64JtaiwncQ6Sd5fhjAEAqIx2FHcaaR5pV+mRZj0mYokFeXrumhiYmb22G7qc4CXMpPFUoJvP+klaO6rtiG0x0HsoEz3BM+rZW3oa9rprVUoTtbbezHJ9dHutWVoUij4ykhQ2J8H3vK0NUZ3hiU1e0MQerqYi7eb/+SQYACORI1T10Jkp6dD0G+VYdR+fm/RX19Mn9JT6fKSnOvvDUdxdyatlxfqpQpH0c7eNoX7UNQBHTvuIbBQDaWS4tfAKAZpVeFdt6pH4W6B7qA7nDJswwPWfmdv/gpzerHL0qqoqYNgbSPo7Odm0DB7BeRxdy1+3HEEYlfQTtk3PqGTXKXipiOtu1Hoiux+T8a+OumAGzUpyL1TQ/IWw0q8m8v6RtRXu2ZFWstZhK45b+tbu5fskjI5l9YKf+6tmOpC2qQjGZEr9vMQGELaZFfB6/qxlo/n6GIACEmIrG2K3O5R2zV8R0AoZlctG1xRAAt6Q70qknfXUAbKNciY8pE9+QZDFNcSWzP7RcsE+EdROFdeDEimMzl8KT338EBp+mqH99QGqtN+9Abo3NX94AgfhG6YSjE7GSZjH6EXYvt2gLsza45ppal9u20N3DBF42/PyBy/zMgQ698sUuhR/lLXN9HXSHYghwSbozEbbWYiAUkyfd7bhzg6cKxWT+qrdNH8NWLSGmojGqUEz6qvrBgf6tWaWHUz8Q85mKYzN7qxn4aYU6vmxP5VrK7d8A+g1uWZJZyjwbYWtaWdLKUiNmHXQjnKIxcnX0gRn2+HTQQnSAyNX1P/qes649hoCJkh7IveDlofXvn93Slz2VkbSyNHS7B3Iv+Mh5a3pWf8aKc3i4EmJeps75XhcHQH8WhMCSH0ZuVOG03msJmlUeGakB3mqsOxd/KIClczAbXPXdhTxavVPn3648H9fAmERW9loZJPTe0lnXHqMKRTrbddx4RLgkfSSLm7/4SymXftuFtmDEK/JZJ/jtd2PPdFympDgXqxk9KteeFpM+rrdLFXYqAOIbtYJxMMLWWmEoYjrxgZc3EHrCH+ynBeN1X8R/neLoDgDdgkZ/Zl9R+3QeVCpGuYgaBPnjuzpAq9V0eHUT3pZv0xR3VtipuOr2Y/buXI7HgXPSRxP/gT/Y3xWoypK1cbC8UgsxlSO7ytItbUiwjfJmCJiu9biP4iQsfPF/CxrnXSqB8D+B/GSMQPAAUngEggd8+VaTQHiAkG88AsEDSOERCB5ACo9A8ID/APlMj2z+wdNTAAAAAElFTkSuQmCC"
with open('sample.png', 'wb') as f:
    f.write(base64.b64decode(image_data_))

# -*- coding: ASCII -*-

# import pythoncom, pyHook

# def OnMouseEvent(event):
#     # called when mouse events are received
#     # print('MessageName:',event.MessageName)
#     # print('Message:',event.Message)
#     # print('Time:',event.Time)
#     # # print( 'Window:',event.Window)
#     # # print( 'WindowName:',event.WindowName)
#     # print('Position:',event.Position)
#     # print('Wheel:',event.Wheel)
#     # print('Injected:',event.Injected)
#     # print('---')

# # return True to pass the event to other handlers
#     return True

# # create a hook manager
# hm = pyHook.HookManager()
# # watch for all mouse events
# hm.MouseAll = OnMouseEvent
# # set the hook
# hm.HookMouse()
# # wait forever
# pythoncom.PumpMessages()

{
   "image":"iVBORw0KGgoAAAANSUhEUgAAACUAAAAeCAIAAAAkQUA6AAAE+ElEQVR4nK1WS4tcVRCuqnO7ZzKPnkmCyeRh0JhIFFcBo0E0wY2KiJBtQsjClYhLlwoi/gBx4R/whzRk6R8IIriJJlnMTD+m+/a9p75yUfecPj2RrHIX3YfzqOdXXxXfvXuXiIiImc2MmdnXREQEVRExs+6I2S/7jh/lh8RM5u+ImA0gIhbxBRENh8PKnzEz/JiZzPLaZeU1EQHw+651qYwIqp0EIjJzmW69q2fmym0EwMzZ3s6L5Lf/ZSmlu2bGIh4Gf+4++WU3wn1wOZULFRG3nYiYKPuUnegeA6Uxfi3L8h0JISvL+zlOkqOxFOSWu43Fl5Uxs4TAyZvjcoEuvavR9rVkM3NIKVlNzDBjEUoPSjs8WzkSrsCPNKXfwVGmRkpnu5CmxBjALrcw1u8Y4AkrVbJI90tkZgqwCAA3xYHWxaRENhFpQlrncTL/jfdvkdmVm7eZ+fJ7H5nZlZu3zez1Gx+6ER6JEAIzBxGXzCIsIiIAOmSraggh10OX86Lgbnz17bN5+9mdO08m81tffPlkMr/+6edPp/XVjz95drTYfveD619/d+VsA1UDHLTuFBEZ4JtExPfu3ctACCIKCDMACcErhpirXu+tB9/ceedqCywUC0WtmEedR521sY7678HhmnB/+MsfjyKl6ioR7kY/fPjQQ94lzPNMzK4sp2p770LVNjAABJjCFNAugqawGPXUifVcG0uqSpBJgLVKk6c5+aoqhXXMPLh0uR/r/dG4NWsVdcRCtY5aA/NWj9o4Gh1e292YFnXZkUtWGYIBqlqVxfu8Ua6yd+a8NPXG1nYLNDCJkRUU1aIiom2i9CbXLuw9JSLPRVGaziEOCDOrsrNZsThZJ8Yjompnlw+fHYzHraJR1KpNRA3MWl0opm17NJnssDk0PCN0jArMvH4qV7ukPq/xdIOIpN9nokh2YnOzUoiCFBwVqohq0UI939ndufTKqSxKVTkpy9jxaFVlMKloNBlXm+cvVW3bRD0YjReKRrVR1J7FqDPo0XRexXY0mWRvgpdsQkYWa2ZVVpOto6LpmNnWq6/x4kiN1rc2OYIjDIqoiKYxVqq9aGdODE4OBtkJD2xGilMjmxFRVWauBFXe7J89r7MpzPYPx61ioVoDTUQdUavOWtST8eWN0wfjsePCgExpnLtukl+tNjty1injHja329E+Qm9tY8MiVFEpYoyikAgJsWoWb1885/55I4SqhMAppB1bOT6f5wIp2ke1uSVmLFxVYTadNooG1ijaqBFmqqQ6GY0GYu4fETlDdV6mUHEqjEpEhBnFPJIrwczW9y6GwW5v91Q/yOPIZoHIEAJJtSayRrSuWDTxzXNncngo5S/XXwjBfJBxvGhO8mq/FpHZ338++vVnf/n9jz+dPn2S/ufby86ZGRUjhfuwnIzyPLECXKJM2Xk+Y+bff/vh5OB40y+//f0p81o22rsEFZKJqGJmYY6quea8by2HnJTev/5RexxXRpUErrTTF2EFMgKtQHvH0sysQH4pIkhEmt+4MKT25PvMrKrHuNDS0TE1HtIQwpKUJfX+LvrF5NmRTgjeQrsZYHVWA+CjbRDJrW2JeREiUlUphbp/UkzE2TTXlOclM/OhIRvnr7q27qSf4mTFfNvNE5lWAFAaOMu26Ty+Ag8zV+MDFVLYyflzFaJe8gCq+/fvvwByL/cbDocvwvdL/5j5P+Fwsn/uGAxLAAAAAElFTkSuQmCC",
   "mouse_coords":{
      "x":640,
      "y":1069
   },
   "path":{
      "0":{
         "automation_id":"{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\\notepad.exe",
         "class_name":"",
         "control_type":"Button",
         "handle":"None",
         "parent_index":0,
         "title":"Блокнот\\xa0—1 запущенное окно",
         "top_parent_index":0
      },
      "1":{
         "automation_id":"",
         "class_name":"MSTaskListWClass",
         "control_type":"ToolBar",
         "handle":65804,
         "parent_index":0,
         "title":"Работающие приложения",
         "top_parent_index":0
      },
      "2":{
         "class_name":"Shell_TrayWnd",
         "control_type":"Pane",
         "title":"Панель задач"
      }
   },
   "rect":{
      "B":1080,
      "L":629,
      "R":666,
      "T":1050
   }
}