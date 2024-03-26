import sqlparse
from sqlparse.sql import Identifier, IdentifierList, Function
from sqlparse.tokens import Keyword, DML, Name

class SQLExtractor:
    def __init__(self, sql):
        self.sql = sql
        self.parsed = sqlparse.parse(self.sql)[0]
        self.columns = []
        self.table_names = []

    def extract(self):
        self._extract_table_names()
        self._recursively_extract_columns(self.parsed)
        # アスタリスク(*)、テーブル名、FROM句内のテーブル名、関数を含むカラム名を除外
        self.columns = [
            col for col in self.columns if col not in ('*',) 
            and '.' not in col 
            and col not in self.table_names 
            and not self._is_function(col)
        ]
        return self.columns, self.table_names

    def _extract_table_names(self):
        # FROM句に基づくテーブル名の抽出
        from_seen = False
        for token in self.parsed.tokens:
            if from_seen and isinstance(token, IdentifierList):
                for identifier in token.get_identifiers():
                    self.table_names.append(str(identifier))
            elif from_seen and isinstance(token, Identifier):
                self.table_names.append(str(token))
            elif token.ttype is Keyword and token.value.upper() == 'FROM':
                from_seen = True

    def _recursively_extract_columns(self, token_list):
        for token in token_list.tokens:
            if isinstance(token, Function):
                # 関数内のカラム名も考慮する場合はここで処理
                continue
            if token.is_group:
                self._recursively_extract_columns(token)
            elif isinstance(token, Identifier) \
                and token.get_real_name() \
                and not isinstance(token.parent, Function):
                self.columns.append(token.get_real_name())
            elif token.ttype == Name and not isinstance(token.parent, Function):
                self.columns.append(str(token).strip())

    def _is_function(self, column_name):
        # 関数かどうかを識別する簡易的な方法
        # ここでは実装されていませんが、カラム名が実際に関数名であるかどうかをチェックするロジックを追加できます
        return False

# 使用例
sql = "SELECT users.id, users.name, count(*) FROM users WHERE age > 20 AND status = 'active'"
extractor = SQLExtractor(sql)
columns, table_names = extractor.extract()
print("Columns:", columns)
print("Tables:", table_names)
