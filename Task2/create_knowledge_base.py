import os
import json

def replace_names(text_content: str) -> str:
    path = os.path.join('.', 'Task2', 'terms_map.json')
    with open(path, 'r') as dict_file:
        terms_map = json.load(dict_file)
        
        for original_name in terms_map:
            text_content = text_content.replace(original_name, terms_map[original_name])
            text_content = text_content.replace(original_name.lower(), terms_map[original_name].lower())

    return text_content

if __name__ == '__main__':

    dir_raw = os.path.join('.', 'Task2', 'raw')
    txt_files = [f for f in os.listdir(dir_raw) if f.endswith('.txt')]

    directory = os.path.join('.', 'Task4-5', 'knowledge_base')
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    for filename in txt_files:
        path_cur_raw_file = os.path.join(dir_raw, filename)
        with open(path_cur_raw_file, 'r', encoding='utf-8') as f:
            text = f.read()

            text = text.replace('[]', ' ').replace('\n', ' ').strip()

            text_content = replace_names(text)

            path = os.path.join(directory, filename)
            print(path)
            with open(path, 'w') as file:
                file.write(text_content)