import pandas as pd
ls_extensions = ["py", "ipynb", "md", "csv", "png"]

from .my_ui import MyUI
from .my_file_list import MyFileList
from .my_data_frame import MyDataFrame
from .power_in_file_search import PowerInFileSearch

mu = MyUI
my_input = lambda x,y: mu.input(x,y)


class MySearch:
    def __init__(self, tar_dir=".", extensions=ls_extensions):
        mfl = MyFileList(tar_dir)
        mfl.get_df_file_list(extensions=extensions)
        self.mfl = mfl
        
    def search_files_core(self, tar_str, tar_cols, ls_extensions, flg_refresh, flg_regex):
        mfl = self.mfl
        if flg_refresh:
            mfl.get_df_file_list(extensions=ls_extensions)
        df = mfl.df_file_list.sort_values('last_update', ascending = False).reset_index(drop=True)
        mdf = MyDataFrame(df)
        df_filter = mdf.search(tar_str, tar_cols, flg_regex=flg_regex)
        mfl.show(df_filter)
        self.mfl = mfl
    
    def search_files_ui(self):
        tar_str = my_input("search: ", "*")
        
        ls_cols = ['file_name', 'dir_name']
        tar_cols = my_input(f"in which fields? (dafault: '{', '.join(ls_cols)}') :", ls_cols)
        tar_cols = tar_cols if isinstance(tar_cols, list) else [tar_cols]
    
        res = [tar_str, tar_cols]
        return res
    
    def search_files(self, flg_refresh = True, flg_regex=True):
        mfl = self.mfl
        [tar_str, tar_cols] = self.search_files_ui()
        self.search_files_core(tar_str, tar_cols, ls_extensions, flg_refresh, flg_regex)

    def show_md_ui(self):
        mdf = MyDataFrame(self.mfl.df_show)
        idx = mdf.search("md", "extension").index[0]
        idx = int(my_input(f"input md file index: (default={idx})", idx))
        return idx

    def show_md(self):
        mfl = self.mfl
        idx = self.show_md_ui()
        mfl.idx = idx
        print(f"display: {mfl.file_path}")
        mfl.show_md_file(idx)
"""
    def search(self, keywords, mode="or", file_list = None, case_sensitive=False):
        
        if file_list:
            pass
        elif 
        ifs = PowerInFileSearch(file_list, case_sensitive)
"""        


    
