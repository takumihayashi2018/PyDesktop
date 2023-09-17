from IPython.display import display, Markdown, HTML

class MyMdLinks:
    def __init__(self, files):
        self._files = files
        self._file = files[0]
        self._str_md = ""

    @property
    def files(self):
        return self._files

    @files.setter
    def files(self, value):
        self._files = value

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, value):
        self._file = value

    @property
    def str_md(self):
        return self._str_md

    @str_md.setter
    def str_md(self, value):
        self._str_md = value
        
    def load(self):
        self.file

    def show(self):
        display(Markdown(self.str_md))

        
def md_display(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    display(Markdown(content))
