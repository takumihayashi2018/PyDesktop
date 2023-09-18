import ipywidgets as widgets
from IPython.display import display, clear_output
from typing import Callable, List

class MyButtons:
    def __init__(self, func: Callable[..., None], ls_buttons: List[str], flg_Vertical=True):
        self.ls_buttons = ls_buttons
        self.func = func
        self.idx = None
        self.buttons = [widgets.Button(description=desc) for desc in ls_buttons]
        
        for idx, button in enumerate(self.buttons):
            button.on_click(lambda btn, i=idx: self.action(i))

        # ボタンの配置 (垂直 or 水平)
        if flg_Vertical:
            self.button_box = widgets.VBox(self.buttons)
        else:
            self.button_box = widgets.HBox(self.buttons)

        # 出力ウィジェットの作成
        self.output = widgets.Output()

    def action(self, index):
        self.idx = index
        with self.output:
            clear_output(wait=True)
            self.func(index)

    def show(self):
        display(self.button_box, self.output)
