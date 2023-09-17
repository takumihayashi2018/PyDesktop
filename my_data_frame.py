import pandas as pd
import re

class MyDataFrame:
    def __init__(self, dataframe=None):
        self.df = dataframe.copy() if dataframe is not None else None
        self.df_res = None

    def search(self, query, columns=None, operator='or', flg_regex=False, flg_ignorecase=True, df=None):
        if df is not None:
            self.df = df.copy()
        
        if query == "*":
            return self.df 

        if self.df is None:
            raise ValueError("DataFrame is not set. Please provide a DataFrame.")

        if columns is None:
            columns = list(self.df.columns)
        columns = columns if isinstance(columns, list) else [columns]
        
        if flg_ignorecase:
            query = query.lower()

        if operator not in ['or', 'and']:
            raise ValueError("Operator must be 'or' or 'and'.")

        if operator == 'or':
            filtered_df = pd.DataFrame()
            for col in columns:
                if flg_regex:
                    if flg_ignorecase:
                        matches = self.df[self.df[col].str.lower().str.contains(query, regex=True, na=False)]
                    else:
                        matches = self.df[self.df[col].str.contains(query, regex=True, na=False)]
                else:
                    if flg_ignorecase:
                        matches = self.df[self.df[col].str.lower().str.contains(re.escape(query), regex=True, na=False)]
                    else:
                        matches = self.df[self.df[col].str.contains(re.escape(query), regex=True, na=False)]
                filtered_df = pd.concat([filtered_df, matches], axis=0)
            self.df_res = filtered_df.drop_duplicates()
            return self.df_res

        if operator == 'and':
            filtered_df = self.df
            for col in columns:
                if flg_regex:
                    if flg_ignorecase:
                        filtered_df = filtered_df[filtered_df[col].str.lower().str.contains(query, regex=True, na=False)]
                    else:
                        filtered_df = filtered_df[filtered_df[col].str.contains(query, regex=True, na=False)]
                else:
                    if flg_ignorecase:
                        filtered_df = filtered_df[filtered_df[col].str.lower().str.contains(re.escape(query), regex=True, na=False)]
                    else:
                        filtered_df = filtered_df[filtered_df[col].str.contains(re.escape(query), regex=True, na=False)]
            self.df_res = filtered_df
            return self.df_res


