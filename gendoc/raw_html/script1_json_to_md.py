from pathlib import Path
import json

build_folder = Path('build')
build_folder.mkdir(exist_ok=True)

input_file = Path('../build/content.json')
assert input_file.exists()

content = json.load(open(input_file, 'r'))

f = open(build_folder / 'index.md', 'w')
f.write('# PyTorch C++ Cheatsheet\n\n')

for it in content:
    sec_title = it[0]
    sec_content = it[1]
    f.write('## ' + sec_title + '\n\n')
       
    for type_str,lines in sec_content:
        if type_str == 'code':
            f.write('```c++\n')
        for l in lines:
            f.write(l)
            f.write('\n')
        if type_str == 'code':
            f.write('```\n')
        f.write('\n')