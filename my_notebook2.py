import os
import nbformat as nbf
from IPython.display import display, HTML

class MyNotebook:
    def __init__(self, template_filename="nb_templates.ipynb"):
        self.nb = nbf.v4.new_notebook()
        self.template_filename = template_filename

    def add_code_cell(self, code_content):
        code_cell = nbf.v4.new_code_cell(code_content)
        self.nb.cells.append(code_cell)

    def add_markdown_cell(self, md_content):
        md_cell = nbf.v4.new_markdown_cell(md_content)
        self.nb.cells.append(md_cell)

    def get_available_templates(self):
        """利用可能なテンプレートのIDリストを取得する"""
        with open(self.template_filename, 'r', encoding='utf-8') as f:
            template_nb = nbf.read(f, as_version=4)
            
            template_ids = []
            for cell in template_nb.cells:
                if cell.source.startswith("# TEMPLATE_ID: "):
                    template_id = cell.source.split(":")[1].strip()
                    template_ids.append(template_id)
            return template_ids

    def new(self, template_id=None, output_filename=None):
        """テンプレートIDを選択して、新しいノートブックを作成し保存する"""
        available_template_ids = self.get_available_templates()
        
        if template_id is None:
            print("Available template IDs:", ", ".join(available_template_ids))
            template_id = input("Enter the template ID you want to use: ")
        
        with open(self.template_filename, 'r', encoding='utf-8') as f:
            template_nb = nbf.read(f, as_version=4)
            
            is_target_template = False
            for cell in template_nb.cells:
                if cell.source.startswith(f"# TEMPLATE_ID: {template_id}"):
                    is_target_template = True
                if is_target_template:
                    if cell.cell_type == 'code':
                        self.add_code_cell(cell.source)
                    elif cell.cell_type == 'markdown':
                        self.add_markdown_cell(cell.source)
                    if cell.source.startswith("# TEMPLATE_ID: ") and cell.source != f"# TEMPLATE_ID: {template_id}":
                        break
        
        if output_filename is None:
            output_filename = input("Enter the filename to save the new notebook: ")
        output_filename = self._normalize_filename(output_filename)
        
        if os.path.exists(output_filename):
            overwrite = input(f"{output_filename} already exists. Do you want to overwrite? (y/n): ")
            if overwrite.lower() != 'y':
                print("Aborted.")
                return
        
        self.save_to_file(output_filename)

    def _normalize_filename(self, filename):
        """ファイル名の拡張子を正規化する（.ipynbにする）"""
        if not filename.endswith(".ipynb"):
            if "." in filename:
                filename = filename.rsplit(".", 1)[0]
            filename += ".ipynb"
        return filename

    def save_to_file(self, notebook_filename):
        with open(notebook_filename, 'w', encoding='utf-8') as f:
            nbf.write(self.nb, f)
        
        # ファイルへのリンクを出力
        link_text = f"New Note File Link: <a href='{notebook_filename}' target='_blank'>{notebook_filename}</a>"
        display(HTML(link_text))

# 使用例
notebook = MyNotebook()
notebook.new()



''''
# TEMPLATE_ID: 001
# This is a markdown cell for template 001.

print("This is a code cell for template 001.")

# TEMPLATE_ID: 002
# This is a markdown cell for template 002.

print("This is a code cell for template 002.")
''''