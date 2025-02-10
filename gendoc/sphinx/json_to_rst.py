from pathlib import Path
import json

build_folder = Path('build')
build_folder.mkdir(exist_ok=True)

input_file = Path('../build/content.json')
assert input_file.exists()

content = json.load(open(input_file, 'r'))

f = open('source/index.rst', 'w')

f.write('PyTorch C++ Cheatsheet\n')
f.write('======================\n')
f.write('\n')

for it in content:
    sec_title = it[0]
    sec_content = it[1]
    
    f.write(sec_title)
    f.write('\n')
    f.write('-' * len(sec_title))
    f.write('\n\n')
       
    for type_str,lines in sec_content:
        if type_str == 'code':
            f.write('.. code-block:: cpp\n\n')
        for l in lines:
            if type_str == 'code':
                f.write('    ')
            f.write(l)
            f.write('\n')
        f.write('\n')