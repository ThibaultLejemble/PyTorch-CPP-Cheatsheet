#/bin/bash
 
set -ex

cp raw_html_style.css build/raw_html_style.css
pandoc --standalone --metadata pagetitle="PyTorch C++ Cheatsheet" build/index.md -o build/index.html --css=raw_html_style.css
