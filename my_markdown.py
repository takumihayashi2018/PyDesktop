from IPython.display import display, FileLink, Markdown

class MyMarkdown:
    def __init__(self):
        self.content = ""
        
    def show(self):
        display(Markdown(self.tmpcontent))
        
    def showall(self):
        display(Markdown(self.content)) 

    def refresh(self, md_str=None):
        if not md_str:
            self.content = ""
            self.tmpcontent = ""
            return self
        self.content += md_str
        self.tmpcontent = md_str
        

    def header(self, text, level=1):
        formatted = "#" * level + " " + text + "\n\n"
        self.refresh(formatted)
        return self

    def paragraph(self, text):
        formatted = text + "\n\n"
        self.refresh(formatted)
        return self

    def br(self, text=""):
        if text == "":
            formatted = "  \n"
            self.refresh(formatted)
            return self
        lines = text.split("\n")
        trimmed_lines = [line.rstrip() for line in lines]
        formatted_text = "  \n".join(trimmed_lines)
        formated = formatted_text + "\n\n"
        self.refresh(formatted)
        return self

    def bold(self, text):
        formatted = f"**{text}**"
        self.refresh(formatted)
        return self

    def italic(self, text):
        formatted = f"*{text}*"
        self.refresh(formatted)
        return self
        
    def bullet(self, text=""):
        formatted = f"- {text}"
        self.refresh(formatted)
        return self

    def bullet_list(self, items):
        items = items if isinstance(items, list) else [items]
        formatted = "\n".join(["- " + item for item in items]) + "\n\n"
        self.refresh(formatted)
        return self

    def numbered_list(self, items):
        items = items if isinstance(items, list) else [items]
        formatted = "\n".join([f"{i}. {item}" for i, item in enumerate(items, 1)]) + "\n\n"
        self.refresh(formatted)
        return self

    def link(self, text, url):
        formatted = f"[{text}]({url})"
        self.refresh(formatted)
        return self

    def image(self, url, alt_text = "image", width="auto", height="auto", align="left"):       
        formatted = f'<img src="{url}" alt="{alt_text}" width={width} height={height} align={align}>\n\n'
        self.refresh(formatted)
        return self

    def font_color(self, text, color):
        formatted = f'<span style="color:{color}">{text}</span>'
        self.refresh(formatted)
        return self

    def background_color(self, text, color):
        formatted = f'<span style="background-color:{color}">{text}</span>'
        self.refresh(formatted)
        return self

    def font_size(self, text, size):
        formatted = f'<span style="font-size:{size}">{text}</span>'
        self.refresh(formatted)
        return self

    def underline(self, text):
        formatted = f'<u>{text}</u>'
        self.refresh(formatted)
        return self

    def inline_math(self, equation):
        formatted = f"${equation}$"
        self.refresh(formatted)
        return self

    def block_math(self, equation):
        formatted = f"$$\n{equation}\n$$\n\n"
        self.refresh(formatted)
        return self
        
    def load(self, markdown_file):
        with open(markdown_file, 'r', encoding='utf-8') as f:
            formatted = f.read()
        self.refresh(formatted)
        return self
        

    def __str__(self):
        return self.content

    def pynb2md(self, notebook_path=None, output_md_path=None):
        """Converts a Jupyter Notebook to a Markdown file."""
        
        if not notebook_path:
            notebook_path = input("Please enter the path to the Jupyter Notebook: ")

        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)

        # マークダウンセルの内容を結合
        for cell in notebook['cells']:
            if cell['cell_type'] == 'markdown':
                self.md_contents += cell['source'][0] + "\n\n"
                
        # 出力先の.mdファイルが指定されている場合、ファイルに内容を書き出す
        if output_md_path:
            with open(output_md_path, 'w', encoding='utf-8') as f:
                f.write(self.md_contents)

        return self





class ConfluenceToMarkdown:
    def __init__(self, content):
        self.content = content

    def convert_headers(self):
        for i in range(6, 0, -1):
            self.content = self.content.replace('h{}. '.format(i), '#' * i + ' ')

    def convert_bold(self):
        self.content = self.content.replace('*', '**')

    def convert_italics(self):
        self.content = self.content.replace('_', '*')

    def convert_lists(self):
        self.content = self.content.replace('* ', '- ')

    def convert_links(self):
        import re
        self.content = re.sub(r'\[(.*?)\|(.*?)\]', r'[\1](\2)', self.content)

    def handle_newlines(self):
        # 各行の末尾の空白を削除し、2つの空白を追加してマークダウンでの改行を表現
        self.content = '\n'.join([line.rstrip() + '  ' if line.strip() != '' else line for line in self.content.split('\n')])

    def convert(self):
        self.convert_headers()
        self.convert_bold()
        self.convert_italics()
        self.convert_lists()
        self.convert_links()
        self.handle_newlines()
        return self.content




