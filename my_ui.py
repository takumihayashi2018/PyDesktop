

class MyUI:
    def input(prompt, default_value=None):
        '''
        - input関数にデフォルト値を持たせる。
        - カンマ区切りの文字列を、リストとして認識する。
        '''
        value = input(prompt)
        if not value:
            return default_value
        
        if ',' in value:
            
            return [item.strip() for item in value.split(',')]
        return value