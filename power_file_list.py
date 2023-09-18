import os
import pandas as pd
from datetime import datetime, timedelta
import re
from concurrent.futures import ThreadPoolExecutor
from IPython.display import display, Markdown
import time  # 実行時間計測のため

pd.options.display.colheader_justify = 'left'

ndays = 5
dirs_outscope = ['lib', 'nouse', 'venv']
ls_extensions = ['ipynb', 'py', 'md']


class PowerFileList:
    def __init__(self, base_dir='.'):
        self.df_file_list = pd.DataFrame()
        self._base_dir = base_dir
        self.idx = 0

    @property
    def base_dir(self):
        return self._base_dir

    @base_dir.setter
    def base_dir(self, base_dir):
        self._base_dir = base_dir

    @property
    def update_flg_time(self):
        return re.sub(r'\.\d+', '', str(datetime.now() - timedelta(days=self.ndays)))
    
    def _process_directory(self, base_depth, directory_data):
        dirpath, dirnames, filenames = directory_data
        file_data = []
    
        # dirs_outscopeのディレクトリやその子孫をスキップ
        if any(os.path.join(self._base_dir, dir_out) in dirpath for dir_out in self.dir_out_scope):
            dirnames[:] = []  # このディレクトリ以下の走査をスキップ
            return []
    
        # .で始まる隠しディレクトリをスキップ
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]

        if any(dir_out in dirpath for dir_out in self.dir_out_scope):
            return []

        for filename in filenames:
            file_ext = os.path.splitext(filename)[1][1:]
            if file_ext in self.extensions:
                full_path = os.path.join(dirpath, filename)
                directory_name = os.path.basename(os.path.dirname(full_path))
                last_update_timestamp = os.path.getmtime(full_path)
                last_update_date = datetime.fromtimestamp(last_update_timestamp)
                last_update_date_str = re.sub(r'\.\d+', '', str(last_update_date))
                flg_updated = (datetime.now() - last_update_date) <= timedelta(days=self.ndays)
                current_depth = dirpath.rstrip(os.path.sep).count(os.path.sep) - base_depth
                file_data.append({
                    'file_name': filename,
                    'dir_path': dirpath,
                    'dir_name': directory_name,
                    'extension': file_ext,
                    'last_update': last_update_date_str,
                    'flg_updated': flg_updated,
                    'depth': current_depth
                })
        return file_data

    def get_df_file_list(self, base_dir='', extensions=ls_extensions, ndays=ndays, dir_out_scope=dirs_outscope):
        start_time = time.time()  # 実行時間計測の開始

        self.extensions = extensions
        self.dir_out_scope = dir_out_scope
        self.ndays = ndays

        if base_dir != '':
            self.base_dir = base_dir
        base_dir = self.base_dir

        base_depth = base_dir.rstrip(os.path.sep).count(os.path.sep)
        all_file_data = []

        directories = list(os.walk(base_dir))

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self._process_directory, base_depth, directory) for directory in directories]

            for future in futures:
                all_file_data.extend(future.result())

        cols = ['file_name', 'dir_path', 'dir_name', 'extension', 'last_update', 'flg_updated', 'depth']
        df = pd.DataFrame(all_file_data, columns=cols)
        df['link'] = df.apply(lambda x: f'<a href="{x.dir_path}/{x.file_name}">link</a>', axis=1)
        cols = ["link"] + cols
        df['tmp_file_name'] = df.file_name.str.lower()
        df['tmp_dir_path'] = df.dir_path.str.lower()
        df = df.sort_values(by=['tmp_dir_path', 'depth', 'tmp_file_name']).drop(
            columns=['tmp_dir_path', 'tmp_file_name']).reset_index(drop=True)
        self.df_file_list = self.df_show = df[cols]
        self.updated_time = re.sub(r'\.\d+', '', str(datetime.now()))

        end_time = time.time()  # 実行時間計測の終了
        print(f"Execution Time: {end_time - start_time:.2f} seconds")

    @property
    def df_updated_only(self):
        return self.df_file_list.query("flg_updated == True").sort_values("last_update", ascending = False)
    
    def show(self, df=None):
        if df is None:
            df = self.df_file_list
        
        ls_cols = ['file_name', 'dir_path', 'dir_name', 'extension']
        display(df.style.set_properties(subset=ls_cols, **{'text-align': 'left'}))
        self.df_show = df

    @property
    def file_path(self):
        return f"{self.dir_path}/{self.file_name}"

    @property
    def file_name(self):
        return self.df_show['file_name'][self.idx]
    
    @property
    def dir_path(self):
        return self.df_show['dir_path'][self.idx]
        
    @property
    def dir_name(self):
        return self.df_show['dir_name'][self.idx]
        
    def show_md_file(self, idx = 0):
        self.idx = idx
        with open(self.file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        display(Markdown(content))

    def get_file_path(self, idx=0):
        self.idx = idx
        return self.file_path

    def opendir(self, idx=0):
        df = self.df_show
        dir_path = df.dir_path[idx]
        os.system(f'open "{dir_path}"')
    
    def openfile(self, idx=0):
        df = self.df_show
        dir_path = df.dir_path[idx]
        file_name = df.file_name[idx]
        file_path = f"{dir_path}/{file_name}"
        os.system(f'open "{file_path}"')
        
