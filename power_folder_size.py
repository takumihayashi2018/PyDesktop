import os
import pandas as pd
import concurrent.futures
import math

class PowerFolderSize:
    
    def __init__(self, target_folder):
        self.target_folder = target_folder
        self.df = None

    def _convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "K", "M", "G", "T", "P", "E", "Z", "Y")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        size = round(size_bytes / p, 2)
        return size, size_name[i]

    def _get_folder_size(self, dir_path):
        total = 0
        direct_files_total = 0
        max_file_name = ''
        max_file_size = -1

        for subdir, _, files in os.walk(dir_path):
            for f in files:
                fp = os.path.join(subdir, f)
                if not os.path.exists(fp):
                    continue
                file_size = os.path.getsize(fp)
                total += file_size
                if subdir == dir_path:
                    direct_files_total += file_size
                    if file_size > max_file_size:
                        max_file_size = file_size
                        max_file_name = f
        
        return dir_path, total, direct_files_total, max_file_size, max_file_name
    
    def compute(self):
        folder_sizes = []

        all_folders = [dir_path for dir_path, _, _ in os.walk(self.target_folder)]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(self._get_folder_size, all_folders))
        
        for dir_path, total, file_size_total, max_file_size, max_file_name in results:
            dir_name = os.path.basename(dir_path)
            parent_dir = os.path.basename(os.path.dirname(dir_path))
            depth = dir_path[len(self.target_folder):].count(os.sep)
            update_time = max(os.path.getmtime(root) for root, _, _ in os.walk(dir_path))
            update_time = pd.to_datetime(update_time, unit='s').strftime('%Y-%m-%d %H:%M:%S')
            size, unit = self._convert_size(total)
            
            folder_sizes.append({
                'dir_name': dir_name,
                'size_no_unit': total,
                'size': size,
                'unit': unit,
                'file_size_total': file_size_total,
                'max_file_size': max_file_size,
                'max_file_name': max_file_name,
                'parent_dir': parent_dir,
                'dir_path': dir_path,
                'depth': depth,
                'update_time': update_time
            })
        
        self.df = pd.DataFrame(folder_sizes)
