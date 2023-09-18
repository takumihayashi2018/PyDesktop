from typing import Callable
from IPython.display import display, clear_output

from .my_buttons import MyButtons

class MyButtonNextPrev(MyButtons):
    def __init__(self, func: Callable[..., None], idx: int = 0, min_idx: int = 0, max_idx: int = 99999):
        self.index = idx
        self.min_idx = min_idx
        self.max_idx = max_idx
        self.func = func  # ここで func を保存

        # NextとPrevボタンの説明を持つリストを作成
        descriptions = ["Prev", "Next"]

        # MyButtonsのコンストラクタを呼び出してボタンを作成
        super().__init__(self.func, descriptions, flg_Vertical=False)

    def action(self, index):
        # Prevボタンの場合
        if index == 0 and self.index > self.min_idx:
            self.index -= 1
        # Nextボタンの場合
        elif index == 1 and self.index < self.max_idx:
            self.index += 1

        with self.output:
            clear_output(wait=True)
            self.func(self.index)
