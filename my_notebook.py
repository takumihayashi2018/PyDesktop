import nbformat as nbf
import os
from IPython.display import display, HTML, Markdown, FileLink


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
        """利用可能なテンプレートのリストを取得する"""
        with open(self.template_filename, 'r', encoding='utf-8') as f:
            template_nb = nbf.read(f, as_version=4)
            
            templates = set()
            for cell in template_nb.cells:
                if cell.source.startswith("# TEMPLATE: "):
                    template_name = cell.source.split(":")[1].strip()
                    templates.add(template_name)
            return list(templates)


    
    def new(self, idx=None, output_filename=None):
        """テンプレートを選択して、新しいノートブックを作成し保存する"""
        templates = self.get_available_templates()
        
        if idx is None:
            print("Available templates:")
            for i, template_name in enumerate(templates, 1):
                print(f"{i}. {template_name}")
                display(Markdown("---"))
            idx = int(input("Enter the number of the template you want to use: "))
        
        selected_template = templates[idx - 1]
        
        with open(self.template_filename, 'r', encoding='utf-8') as f:
            template_nb = nbf.read(f, as_version=4)
            
            for cell in template_nb.cells:
                if cell.source.startswith(f"# TEMPLATE: {selected_template}"):
                    if cell.cell_type == 'code':
                        self.add_code_cell(cell.source)
                    elif cell.cell_type == 'markdown':
                        self.add_markdown_cell(cell.source)
        
        # 区切りを追加
        self.add_markdown_cell("---")
        
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
        print("New Note File Link: ")
        display(FileLink(notebook_filename))

        #link_text = f"New Note File Link: <a href='{notebook_filename}' target='_blank'>{notebook_filename}</a>"
        #display(HTML(link_text))


