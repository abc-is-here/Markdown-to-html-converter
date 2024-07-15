import re

def parse_markdown_line(line):

    header_match = re.match(r'^(#{1,6})\s*(.+)', line)
    if header_match:
        header_level = len(header_match.group(1))
        header_content = header_match.group(2)
        return f'<h{header_level}>{header_content}</h{header_level}>'
    
    return f'<p>{line}</p>'

def convert_markdown_to_html(markdown_text):
    lines = markdown_text.split('\n')
    html_lines = [parse_markdown_line(line) for line in lines]
    return '\n'.join(html_lines)

markdown_text = """
# Header 1
## Header 2
This is a paragraph.
"""

html_output = convert_markdown_to_html(markdown_text)
print(html_output)
