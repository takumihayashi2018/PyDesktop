import pandas as pd
from IPython.display import display, HTML

class DisplayDfHorisontal:
    def __init__(self, dataframes, headers=None):
        self.dataframes = dataframes
        self.headers = headers if headers else [''] * len(dataframes)
        if len(dataframes) != len(self.headers):
            raise ValueError("The number of headers must match the number of dataframes.")
    
    @staticmethod
    def _color_negative_red(val):
        """Take a scalar and returns a string with css property to color the text red if value is negative"""
        color = 'red' if val < 0 else 'black'
        return f'color: {color}'

    def _style_dataframe(self, df):
        """Style the dataframe: color negative numbers in red"""
        return df.style.applymap(self._color_negative_red).render()

    def _get_header_str(self):
        return '<tr>' + ''.join(f'<th style="text-align:center"><h3>{header}</h3></th>' for header in self.headers) + '</tr>'
    
    def _get_table_str(self):
        return '<tr>' + ''.join(f'<td>{self._style_dataframe(df)}</td>' for df in self.dataframes) + '</tr>'
    
    def display(self):
        display(HTML('<table>' + self._get_header_str() + self._get_table_str() + '</table>'))

