import pandas as pd

class MyClass:
    def __init__(self, data=None):
        if data is None:
            self.df = pd.DataFrame()
        elif isinstance(data, pd.DataFrame):
            self.df = data
        else:
            raise ValueError('Expected a pandas DataFrame')

    def __getattr__(self, name):
        if name in self.df.columns:
            return self.df[name]
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name == 'df':
            super().__setattr__(name, value)
        elif name in self.df.columns:
            self.df[name] = value
        else:
            super().__setattr__(name, value)

    def __repr__(self):
        return str(self.df)

    
    def add_member(self, **kwargs):
        new_data = {k: [v] for k, v in kwargs.items()}
        new_df = pd.DataFrame(new_data)
        self.df = pd.concat([self.df, new_df], ignore_index=True)
        
    def update_member(self, index, **kwargs):
        for key, value in kwargs.items():
            self.df.at[index, key] = value

    def remove_member(self, index):
        self.df.drop(index, inplace=True)
        self.df.reset_index(drop=True, inplace=True)

