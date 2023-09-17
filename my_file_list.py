import os
import pandas as pd
from datetime import datetime, timedelta
import re
from IPython.display import display, HTML, Markdown
pd.options.display.colheader_justify = 'left'

ndays=5
dirs_outscope = ['lib', 'nouse', 'venv']
ls_extensions = ['ipynb', 'py', 'md']

class MyFileList:
    def __init__(self, base_dir='.'):
        self.df_file_list = pd.DataFrame()
        # base_dirを絶対パスに変換
        self._base_dir = os.path.abspath(base_dir)
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
    
    def get_df_file_list(self, base_dir='', extensions=ls_extensions, ndays=ndays, dir_out_scope=dirs_outscope):
        self.ndays = ndays
        if base_dir != '':
            self.base_dir = base_dir
        base_dir = self.base_dir
            
        base_depth = base_dir.rstrip(os.path.sep).count(os.path.sep)
        file_data = []
        for dirpath, dirnames, filenames in os.walk(base_dir):
            # dir_out_scopeに含まれるディレクトリをスキップ
            dirnames[:] = [d for d in dirnames if d not in dir_out_scope and not d.startswith(".")]

            current_depth = dirpath.rstrip(os.path.sep).count(os.path.sep) - base_depth
            for filename in filenames:
                # ファイルの拡張子を取得
                file_ext = os.path.splitext(filename)[1][1:]
                # 拡張子が条件に一致するかを確認
                if file_ext in extensions:
                    full_path = os.path.join(dirpath, filename)
                    directory_name = os.path.basename(os.path.dirname(full_path))
                    last_update_timestamp = os.path.getmtime(full_path)
                    last_update_date = datetime.fromtimestamp(last_update_timestamp)
                    last_update_date_str = re.sub(r'\.\d+', '', str(last_update_date))
                    flg_updated = (datetime.now() - last_update_date) <= timedelta(days=ndays)
                    file_data.append({
                        'file_name': filename,
                        'dir_path': dirpath,
                        'dir_name': directory_name,
                        'extension': file_ext,
                        'last_update': last_update_date_str,
                        'flg_updated': flg_updated,
                        'depth': current_depth
                    })
        cols = ['file_name', 'dir_path', 'dir_name', 'extension', 'last_update', 'flg_updated', 'depth']
        df = pd.DataFrame(file_data, columns=cols)
        # 絶対パスから相対パスに変換してリンクを作成
        df['link'] = df.apply(lambda x: f'<a href="{os.path.relpath(os.path.join(x.dir_path, x.file_name), os.getcwd())}">link</a>', axis=1)
        
        cols = ["link"] + cols
        df['tmp_file_name'] = df.file_name.str.lower()
        df['tmp_dir_path'] = df.dir_path.str.lower()
        df = df.sort_values(by=['tmp_dir_path', 'depth', 'tmp_file_name']).drop(
                columns=['tmp_dir_path', 'tmp_file_name']).reset_index(drop=True)
        self.df_file_list = self.df_show = df[cols]
        self.updated_time = re.sub(r'\.\d+', '', str(datetime.now()))
    
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
        