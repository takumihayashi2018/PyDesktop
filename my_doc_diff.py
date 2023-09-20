import difflib
from IPython.display import display, HTML

class MyDocDiff:
    def __init__(self):
        self.differ = difflib.HtmlDiff()
        self.str_html = ""
        self.doc1 = ""
        self.doc2 = ""

    def load(self, filepath1, filepath2):
        """Load the content of two files into self.doc1 and self.doc2."""
        with open(filepath1, 'r', encoding='utf-8') as f1:
            self.doc1 = f1.read()
        with open(filepath2, 'r', encoding='utf-8') as f2:
            self.doc2 = f2.read()
            
    def compare(self, doc1=None, doc2=None, doc_name1='doc_name1', doc_name2='doc_name2'):
        if not doc1:
            doc1 = self.doc1
            
        if not doc2:
            doc2 = self.doc2
            
        res = self.differ.make_file(doc1.split(), doc2.split(),doc_name1, doc_name2)
        self.str_html = res
        
    def show(self):
        """Display the diff HTML directly in Jupyter or IPython environment."""
        display(HTML(self.str_html))