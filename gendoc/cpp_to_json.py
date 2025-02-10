from pathlib import Path
import json

#
# A section is in the following form:
# 
#    //! ==============================================================
#    //! Section Title
#    //! ==============================================================
#    {
#        //! comment
#        code
#    }
#

build_folder = Path('build')
build_folder.mkdir(exist_ok=True)

input_filename = Path('../pytorch_cpp_cheatsheet.cpp')
f = open(input_filename, 'r')
all_lines = f.readlines()

#
# list[tuple[str,list[str]]]
#
# 0. string: the section title
# 1. list of string: the list of lines (comments + code)
#
content = []

SEP_LINE = '    //! ==============================================================\n'
END_TOKEN = 'return 0;'

# Main loop
idx_line = 0
while True:
    while all_lines[idx_line] != SEP_LINE:
        idx_line += 1
    # 1st sep found
    assert all_lines[idx_line] == SEP_LINE
    idx_line += 1
    # stopping condition
    if all_lines[idx_line].find(END_TOKEN) != -1:
        break
    sec_title = all_lines[idx_line]
    sec_title = sec_title.replace('\n', '')
    sec_title = sec_title.replace('//!', '')
    sec_title = sec_title.lstrip()
    print(sec_title)
    idx_line += 1
    # 2nd sep found
    assert all_lines[idx_line] == SEP_LINE
    idx_line += 1
    sec_lines = []
    while all_lines[idx_line] != SEP_LINE:
        sec_lines.append(all_lines[idx_line])
        idx_line += 1
    # next 1st sep found 
    assert all_lines[idx_line] == SEP_LINE
    content.append((sec_title,sec_lines))

print('======================================')
print('======================================')

#
# same but 
# without open/close braces of begin/end of scope
# without line that include 'TODO'
# without 8-spaces indentation
# without line break at the end
#
content_filtered = []

for it in content:
    print()
    print('______________________')
    sec_title = it[0]
    print(sec_title)
    sec_lines = []
    assert it[1][ 0] == '    {\n'
    assert it[1][-1] == '    }\n'
    for line in it[1][1:-1]:
        assert line[:8] == '        ' or len(line.lstrip())==0
        print(line, end='')
        if line.find('TODO') != -1:
            continue
        if len(line.lstrip())==0:
            sec_lines.append(line.lstrip())
        else:
            sec_lines.append(line[8:].replace('\n', ''))
    content_filtered.append((sec_title,sec_lines))

# 
# same but
# the lines are split in a list of tuple of size 2
# 0. a string equal to 'comment' of 'code'
# 1. a list of string
#  
content_filtered_split = []

for it in content_filtered:
    sec_title = it[0]
    sec_lines = it[1]
    
    sec_lines_split = []
    chunk = []
    commenting = True

    for line in sec_lines:
        is_comment = len(line) > 2 and line[:3] == '//!'
        if (is_comment) and (not commenting):
            # end of code bloc
            if len(chunk) > 0:
                sec_lines_split.append(('code', list(chunk)))
                chunk = []
            commenting = True
        elif (not is_comment) and (commenting):
            # end of comment bloc
            if len(chunk) > 0:
                sec_lines_split.append(('comment', list(chunk)))
                chunk = []
            commenting = False
        if is_comment:
            chunk.append(line[3:])
        else:
            chunk.append(line)
    if len(chunk) > 0: # last chunk
        sec_lines_split.append(('comment' if commenting else 'code', list(chunk)))
        chunk = []
    
    content_filtered_split.append((sec_title,sec_lines_split))
    


with open(build_folder / 'content.json', 'w') as f:
    json.dump(content_filtered_split, f, indent='  ')