#!/usr/bin/python3
import sys
import os
import re
import hashlib

def replace_bold_emphasis(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.*?)__', r'<em>\1</em>', text)
    return text

def convert_md5(text):
    return hashlib.md5(text.encode()).hexdigest()

def remove_c(text):
    return re.sub(r'[cC]', '', text)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        exit(1)
    md_file = sys.argv[1]
    html_file = sys.argv[2]
    
    if not os.path.exists(md_file):
        print(f"Missing {md_file}", file=sys.stderr)
        exit(1)
    
    with open(md_file, 'r') as file:
        lines = file.readlines()
    
    with open(html_file, 'w') as file:
        in_ulist = False
        in_olist = False
        in_paragraph = False
        for line in lines:
            line = line.strip()
            if not line:
                if in_paragraph:
                    file.write("</p>\n")
                    in_paragraph = False
                continue
            
            line = replace_bold_emphasis(line)
            line = re.sub(r'\[\[(.*?)\]\]', lambda x: convert_md5(x.group(1)), line)
            line = re.sub(r'\(\((.*?)\)\)', lambda x: remove_c(x.group(1)), line)
            
            if line.startswith('#'):
                level = line.count('#')
                line = line.lstrip('#').strip()
                if in_paragraph:
                    file.write("</p>\n")
                    in_paragraph = False
                file.write(f"<h{level}>{line}</h{level}>\n")
            elif line.startswith('- '):
                if not in_ulist:
                    if in_paragraph:
                        file.write("</p>\n")
                        in_paragraph = False
                    if in_olist:
                        file.write("</ol>\n")
                        in_olist = False
                    file.write("<ul>\n")
                    in_ulist = True
                line = line.lstrip('- ').strip()
                file.write(f"<li>{line}</li>\n")
            elif line.startswith('* '):
                if not in_olist:
                    if in_paragraph:
                        file.write("</p>\n")
                        in_paragraph = False
                    if in_ulist:
                        file.write("</ul>\n")
                        in_ulist = False
                    file.write("<ol>\n")
                    in_olist = True
                line = line.lstrip('* ').strip()
                file.write(f"<li>{line}</li>\n")
            else:
                if in_ulist:
                    file.write("</ul>\n")
                    in_ulist = False
                if in_olist:
                    file.write("</ol>\n")
                    in_olist = False
                if not in_paragraph:
                    file.write("<p>\n")
                    in_paragraph = True
                file.write(f"{line}<br/>\n")
        if in_paragraph:
            file.write("</p>\n")
        if in_ulist:
            file.write("</ul>\n")
        if in_olist:
            file.write("</ol>\n")
    
    exit(0)
