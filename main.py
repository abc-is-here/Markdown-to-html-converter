import re

def parse_markdown_line(line):
    header_match = re.match(r'^(#{1,6})\s*(.+)', line)
    if header_match:
        header_level = len(header_match.group(1))
        header_content = header_match.group(2)
        return f'<h{header_level}>{header_content}</h{header_level}>'

    if line.startswith('- '):
        return f'<li>{line[2:]}</li>'

    bold_text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)


    italic_text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', bold_text)

    return f'<p>{italic_text}</p>'

def convert_markdown_to_html(markdown_text):

    lines = markdown_text.split('\n')
    html_lines = []

    in_list = False
    for line in lines:
        if line.startswith('- '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(parse_markdown_line(line))
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(parse_markdown_line(line))

    if in_list:
        html_lines.append('</ul>')

    return '\n'.join(html_lines)

markdown_text = """
# Header 1
## Header 2
This is a **bold** paragraph with *italic* text.
- Item 1
- Item 2
- Item 3
"""

html_output = convert_markdown_to_html(markdown_text)
print(html_output)
