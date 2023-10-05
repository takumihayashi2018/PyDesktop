import pandas as pd
from IPython.display import display, HTML

class DisplayDfHorisontal:
    def __init__(self, dataframes, headers=None):
        self.dataframes = dataframes
        self.headers = headers if headers else [''] * len(dataframes)
        if len(dataframes) != len(self.headers):
            raise ValueError("The number of headers must match the number of dataframes.")
    
    def _get_header_str(self):
        return '<tr>' + ''.join(f'<th style="text-align:center"><h3>{header}</h3></th>' for header in self.headers) + '</tr>'
    
    def _get_table_str(self):
        return '<tr>' + ''.join(f'<td>{df.to_html()}</td>' for df in self.dataframes) + '</tr>'
    
    def display(self):
        display(HTML('<table>' + self._get_header_str() + self._get_table_str() + '</table>'))

# 使用例
df1 = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6]
})

df2 = pd.DataFrame({
    'X': [7, 8, 9],
    'Y': [10, 11, 12]
})

df3 = pd.DataFrame({
    'P': [13, 14, 15],
    'Q': [16, 17, 18]
})

df_display = DisplayDfHorisontal([df1, df2, df3], headers=['Header 1', 'Header 2', 'Header 3'])
df_display.display()