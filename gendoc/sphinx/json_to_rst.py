from pathlib import Path
import json

def process_url(line: str) -> str:
    raw_url_to_rst_ref = {
        'https://pytorch.org/cppdocs/notes/tensor_creation.html': 'tensor_creation.html',
        'https://github.com/pytorch/pytorch/blob/69301fb10eb3f7fd49af5c681a2e386af115baba/c10/core/ScalarType.h#L151C12-L151C22': 'ScalarType.h',
        'https://github.com/pytorch/pytorch/blob/69301fb10eb3f7fd49af5c681a2e386af115baba/torch/csrc/api/include/torch/types.h': 'types.h',
        'https://pytorch.org/cppdocs/notes/tensor_basics.html#efficient-access-to-tensor-elements': 'tensor_basics.html',
        'https://pytorch.org/cppdocs/notes/tensor_indexing.html': 'tensor_indexing.html',
    }
    if line.find('https') != -1:
        for raw,ref in raw_url_to_rst_ref.items():
            new_url = f'`{ref} <{raw}>`_'
            line = line.replace(raw,new_url)
    return line

build_folder = Path('build')
build_folder.mkdir(exist_ok=True)

input_file = Path('../build/content.json')
assert input_file.exists()

content = json.load(open(input_file, 'r'))

f = open('source/index.rst', 'w')

f.write('PyTorch C++ Cheatsheet\n')
f.write('======================\n')
f.write('\n')
f.write('.. include:: brief.rst\n')
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
                f.write('    ')
                f.write(l)
                f.write('\n')
        else:
            assert lines[0].replace(' ', '') == ''
            assert lines[-1].replace(' ', '') == ''
            for l in lines[1:-1]:
                f.write('| ')
                f.write(process_url(l))
                f.write('\n')
        f.write('\n')