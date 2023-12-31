import pandas as pd
import concurrent.futures
import os

class PowerInFileSearch:

    def __init__(self, file_list):
        self.file_list = file_list
        self.df = None

    def _search_file(self, file_path, keywords, flg_casesensitive, nrows):
        hits = []
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            for line_num, line in enumerate(lines, 1):
                search_line = line if flg_casesensitive else line.lower()
                for keyword in keywords:
                    search_keyword = keyword if flg_casesensitive else keyword.lower()
                    if search_keyword in search_line:
                        dir_path, file_name = os.path.split(file_path)
                        
                        # 前後の行を含めた内容を取得
                        start_index = max(0, line_num - nrows - 1)
                        end_index = min(len(lines), line_num + nrows - 1)
                        around_lines = lines[start_index:end_index]
                        around_content = ''.join(around_lines).strip()
                        
                        hits.append((file_path, dir_path, file_name, line_num, line.strip(), around_content))
                        break
        return hits

    def search(self, keywords, flg_casesensitive=True, nrows=3):
        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(self._search_file, file_path, keywords, flg_casesensitive, nrows): file_path for file_path in self.file_list}
            for future in concurrent.futures.as_completed(futures):
                results.extend(future.result())

        self.df = pd.DataFrame(results, columns=["file_path", "dir_path", "file_name", "line_number", "line_content", "around_content"])
        self.df["link"] = "<a href='" + self.df["file_path"] + "'>link</a>"

    def show(self):
        if self.df is not None:
            from IPython.display import display, HTML
            display(HTML(self.df.to_html(escape=False)))
        else:
            print("No results to display.")

