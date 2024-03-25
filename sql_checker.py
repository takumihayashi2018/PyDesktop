import sqlparse
from sqlparse.sql import Where, TokenList
from sqlparse.tokens import DML

class SQLSyntaxChecker:
    def __init__(self):
        pass

    def check_sql(self, sql):
        # SQL文をパースする
        parsed = sqlparse.parse(sql)[0]

        # SELECT文のみを許可する
        if not self._is_select_statement(parsed):
            return False, "Only SELECT statements are allowed."
        
        # WHERE節の構文チェック
        where_clause = self._find_where_clause(parsed)
        if where_clause and not self._check_where_clause(where_clause):
            return False, "Invalid WHERE clause syntax."
        
        return True, "Syntax is valid."

    def _is_select_statement(self, parsed):
        # 最初のトークンがSELECT文かどうかをチェック
        return parsed.token_first().match(DML, 'SELECT')

    def _find_where_clause(self, parsed):
        # WHERE節を見つける
        for token in parsed.tokens:
            if isinstance(token, Where):
                return token
        return None

    def _check_where_clause(self, where_clause):
        # WHERE節の構文チェック（この例では簡単なチェックのみ）
        # 実際には、より複雑な構文や条件の検証が必要になる場合があります
        return isinstance(where_clause, TokenList)

# 使用例
checker = SQLSyntaxChecker()
result, message = checker.check_sql("SELECT * FROM users WHERE id = 1")
print(result, message)





import sqlparse
from sqlparse.sql import Identifier, IdentifierList
from sqlparse.tokens import Name, Wildcard

class SQLColumnExtractor:
    def __init__(self):
        pass

    def extract_columns(self, sql):
        # SQL文をパースする
        parsed = sqlparse.parse(sql)[0]
        columns = []
        self._recursively_extract_columns(parsed, columns)
        return columns

    def _recursively_extract_columns(self, token_list, columns):
        for token in token_list.tokens:
            if token.is_group:
                self._recursively_extract_columns(token, columns)
            elif isinstance(token, Identifier) and token.get_real_name():
                columns.append(token.get_real_name())
            elif token.ttype == Name or token.ttype == Wildcard:
                columns.append(str(token).strip())

# 使用例
extractor = SQLColumnExtractor()
columns = extractor.extract_columns("SELECT id, name, count(*) FROM users WHERE age > 20 AND status = 'active'")
print(columns)
