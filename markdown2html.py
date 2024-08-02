#!/usr/bin/python3

import sys
import os
import markdown

def convert_markdown_to_html(input_file, output_file):
    """Convert Markdown file to HTML file."""
    try:
        with open(input_file, 'r') as md_file:
            md_content = md_file.read()
            html_content = markdown.markdown(md_content)
        
        with open(output_file, 'w') as html_file:
            html_file.write(html_content)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        exit(1)

    convert_markdown_to_html(input_file, output_file)
    exit(0)
