import pandas as pd
import concurrent.futures

class PowerInFileSearch:

    def __init__(self, file_list, case_sensitive=False):
        self.file_list = file_list
        self.case_sensitive = case_sensitive

    def _is_binary(self, filename):
        """ Check if file is binary. """
        with open(filename, 'rb') as f:
            for _ in range(512):  # check only the first 512 bytes
                byte = f.read(1)
                if not byte:
                    break
                if byte[0] > 127:
                    return True
        return False

    def _match(self, line, keywords):
        if not self.case_sensitive:
            line = line.lower()
            keywords = [keyword.lower() for keyword in keywords]

        return any(keyword in line for keyword in keywords)

    def _match_in_file(self, file_content, keywords):
        # and search for entire file
        if not self.case_sensitive:
            file_content = file_content.lower()
            keywords = [keyword.lower() for keyword in keywords]

        return all(keyword in file_content for keyword in keywords)

    def _search_file(self, file_path, keywords, mode):
        if self._is_binary(file_path):
            return []

        hits = []
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            file_content = ''.join(lines)

            if mode == "and" and not self._match_in_file(file_content, keywords):
                return hits

            for line_num, line in enumerate(lines, 1):
                if mode == "or" or (mode == "and" and self._match(line, keywords)):
                    before_context = ''.join(lines[max(line_num-4, 0):line_num-1])
                    after_context = ''.join(lines[line_num:min(line_num+2, len(lines))])
                    around_context = before_context + line + after_context
                    hits.append((file_path, line_num, line.strip(), around_context))

        return hits

    def search(self, keywords, mode="or"):
        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(self._search_file, file_path, keywords, mode): file_path for file_path in self.file_list}
            for future in concurrent.futures.as_completed(futures):
                results.extend(future.result())
                
        
        df = pd.DataFrame(results, columns=["file_path", "line_number", "line_content", "around_context"])
        return df

