import os
import nbformat as nbf
import pandas as pd
from IPython.display import display, HTML, clear_output
from .UI.my_ui import MyUI

ui = MyUI()

f_nb_templates = "/Users/takumihayashi/Documents/01_Programming/01_python/96_nb_templates/nb_templates.ipynb"
ls_default_ids = ["COMMON"]

class MyNotebook:
    def __init__(self, template_file_name=f_nb_templates, ls_default_ids=ls_default_ids):
        self.tm = TemplateManager(template_file_name)
        self.ls_template_ids = ls_default_ids
        self.nb = nbf.v4.new_notebook()

    def new(self, output_file_name=None, template_id=None):
        self.tm.get_df_templates()
        
        if not template_id:   
            self.tm.show()
            template_id = input("Enter the template ID you want to use: ")
        clear_output()    
        ls_template_ids = [template_id] + self.ls_template_ids
        self.nb.cells = self.tm.get_template_cells(ls_template_ids)

        if not output_file_name:
            output_file_name = ui.input("Enter the file_name to save the new notebook: ", "new_book.ipynb")
        
        FileOperator.save_as_nb(self.nb, output_file_name)


class TemplateManager:
    TEMPLATE_PREFIX = "# TEMPLATE_ID: "

    def __init__(self, template_file_name):
        self.template_file_name = template_file_name
        self.df_templates = self.get_df_templates()

    def get_df_templates(self):
        with open(self.template_file_name, 'r', encoding='utf-8') as f:
            template_nb = nbf.read(f, as_version=4)

            data = []
            for cell in template_nb.cells:
                if cell.source.startswith(self.TEMPLATE_PREFIX):
                    template_id = cell.source.split("\n")[0].strip().replace(self.TEMPLATE_PREFIX,"")
                    data.append({
                        "template_id": template_id,
                        "code_type": cell.cell_type,
                        "source_script": cell.source,
                        "cell" : cell
                    })
            self.df_templates = df = pd.DataFrame(data)
            return df
            
    def show(self):
        df = self.df_templates
        cols = [col for col in df.columns if col != "cell"]
        self.df_show = df[cols]
        display(self.df_show)

    def get_template_cells(self, ls_template_ids):
        df = self.df_templates
        filtered_templates = df.query(f"template_id in {ls_template_ids}")
        
        cells = []
        for _, row in filtered_templates.iterrows():
            cells.append(row.cell)
        return cells

class FileOperator:
    @staticmethod
    def save_as_nb(notebook, file_name):
        file_name = FileOperator.set_extension(file_name, ".ipynb")
        if not FileOperator.if_overwrite(file_name):
            return False
        with open(file_name, 'w', encoding='utf-8') as f:
            nbf.write(notebook, f)
            
        FileOperator.show_link(file_name)

    @staticmethod
    def if_overwrite(output_file_name):
        if os.path.exists(output_file_name):
            overwrite = input(f"{output_file_name} already exists. Do you want to overwrite? (y/n): ")
            if overwrite.lower() != 'y':
                print("Aborted.")
                return False
            else:
                return True
    
    @staticmethod
    def show_link(file_name):
        link_text = f"File Link: \n<a href='{file_name}' target='_blank'>{file_name}</a>"
        display(HTML(link_text))

    @staticmethod
    def set_extension(file_name, str_extension):
        if not file_name.endswith(str_extension):
            if "." in file_name:
                file_name = file_name.rsplit(".", 1)[0]
            file_name += str_extension
        return file_name

