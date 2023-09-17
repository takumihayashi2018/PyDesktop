from MyModules.useful_functions import *
from IPython.display import display, Markdown
import os
ndays=5
dirs_outscope = ['lib', 'nouse', 'venv']
ls_extensions = ['ipynb', 'py', 'md']

class MarkdownList(MyFileList):

    def __init__(self, base_dir='.'):
        super().__init__(base_dir)
        self._str_md_body = ""
        self._str_md_title = ""
        self._str_markdown = ""
        
    def show(self):
        print(f"last update: {self.updated_time}  \n")
        display(Markdown(self.str_markdown))
    
    def output(self, fout=""):        
        if fout == "":
            fout = f"links.md"
        with open(fout, 'w', encoding='utf-8') as file:
            file.write(f"last update: {self.updated_time}  \n")
            file.write(self.str_markdown)
        print(f"Markdown content saved to {fout}")
    
    @property
    def str_md_title(self):
        return self._str_md_title
    
    @property
    def str_md_body(self):
        return self._str_md_body
    
    @property
    def str_markdown(self):
        self._str_markdown = self.str_md_title + self.str_md_body
        return self._str_markdown
    
    @str_markdown.setter
    def str_markdown(self, str_markdown=""):
        if str_markdown != "":
            self._str_markdown = str_markdown
        else:
            self._str_markdown = self.str_md_title + self.str_md_body
    
    def generate_links(self, base_dir='', extensions=ls_extensions, ndays=ndays
                                , dir_out_scope=dirs_outscope):
        self._generate_links(base_dir, extensions, ndays, dir_out_scope, False)
        str_title = f"<span><b>File links under '{self.base_dir}'</b></span></br>updated mark if updated after {self.update_flg_time}':  </br>"
        self._str_md_title = str_title
    
    def generate_updated_links(self, base_dir='', extensions=ls_extensions, ndays=ndays
                                , dir_out_scope=dirs_outscope):        
        self._generate_links(base_dir, extensions, ndays, dir_out_scope, True)
        str_title = f"<span><b>Updated file links under '{self.base_dir}'</b></span></br>since {self.update_flg_time}:  </br>"
        self._str_md_title = str_title
    
    def _generate_links(self, base_dir='', extensions=ls_extensions, ndays=ndays
                                , dir_out_scope=dirs_outscope, flg_updated_only=False):
        
        self.get_df_file_list(base_dir, extensions, ndays, dir_out_scope)
        
        if flg_updated_only:
            flg_str_update=False
            df = self.df_updated_only
        else:
            flg_str_update=True
            df = self.df_file_list.copy()

        str_markdown = ""
        prev_depth = 0
        prev_dir = ""

        for index, row in df.iterrows():
            if row['dir_path'] != prev_dir: 
                display_path = row['dir_path'].replace(self.base_dir, '', 1)
                if display_path == "":
                    display_path = "base_dir"
                if display_path.startswith('/'):
                    display_path = display_path[1:]

                str_markdown += f"<span>{display_path}</span></br>"
                prev_dir = row['dir_path']
            
            # indentation
            str_markdown += "<span style=color:white>" + "--" * row['depth'] + "</span>"
            
            # Add the file link to the markdown string
            str_markdown += "- [{}]({})".format(row['file_name'], os.path.join(row['dir_path'], row['file_name']))
            nline = max(0, 30 - len(row['file_name']))
            str_markdown += f" <span style=color:gray>{'-' * nline} (updated at: {row['last_update']})</span>"
            # If recently updated, append "Updated!!" in red
            if flg_str_update and row['flg_updated']:
                str_markdown += " <span style='color:red'>Updated!!</span>"
            
            str_markdown += "</br>"

            prev_depth = row['depth']
        self._str_md_body = str_markdown
