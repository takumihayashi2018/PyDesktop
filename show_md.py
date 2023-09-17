from IPython.display import display, Markdown

def show_md(file_paths):
    if str(file_paths) == str:
        file_paths = [file_paths]
    for file_path in file_paths:    
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        display(Markdown(content))
