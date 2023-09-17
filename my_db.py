import sqlite3
import pandas as pd

class MyDB:
    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.conn.close()

    def create_table(self, table_name, schema, primary_key=None):
        with self.conn:
            if primary_key:
                query = f"CREATE TABLE IF NOT EXISTS {table_name} ({schema}, PRIMARY KEY({primary_key}))"
            else:
                query = f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})"
            self.conn.execute(query)

    def insert_data(self, table_name, df):
        with self.conn:
            df.to_sql(table_name, self.conn, if_exists='append', index=False)

    def query_data(self, query):
        return pd.read_sql_query(query, self.conn)

    def update_data(self, table_name, df, condition_column):
        with self.conn:
            for _, row in df.iterrows():
                set_clause = ", ".join(f"{col} = '{row[col]}'" for col in df.columns if col != condition_column)
                condition = f"{condition_column} = '{row[condition_column]}'"
                query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
                self.conn.execute(query)


class MyTable(MyDB):
    def __init__(self, db_name, table_name):
        super().__init__(db_name)
        self.table_name = table_name

    def insert(self, df):
        self.insert_data(self.table_name, df)

    def select(self, condition=None):
        query = f"SELECT * FROM {self.table_name}"
        if condition:
            query += f" WHERE {condition}"
        return self.query_data(query)

    def update(self, df, condition_column):
        self.update_data(self.table_name, df, condition_column)

    def delete(self, condition):
        with self.conn:
            query = f"DELETE FROM {self.table_name} WHERE {condition}"
            self.conn.execute(query)

# 使用例:
with MyTable('test.db', 'sample') as table:
    table.create_table('id INTEGER, name TEXT', primary_key='id')
    df_insert = pd.DataFrame({'id': [1, 2], 'name': ['Alice', 'Bob']})
    table.insert(df_insert)
    print(table.select())
    
    df_update = pd.DataFrame({'id': [2], 'name': ['Charlie']})
    table.update(df_update, 'id')
    print(table.select())
    
    table.delete('id=1')
    print(table.select())
