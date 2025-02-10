#/bin/bash
 
set -ex
 
python3 cpp_to_json.py
cd sphinx/
python3 json_to_rst.py
make html
cp -r build/html ../../docs