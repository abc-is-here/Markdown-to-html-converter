import re
import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Markdown files", "*.md")])
    if file_path:
        with open(file_path, 'r') as file:
            markdown_text = file.read()
            markdown_textbox.delete(1.0, tk.END)
            markdown_textbox.insert(tk.END, markdown_text)

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
    if file_path:
        html_output = convert_markdown_to_html(markdown_textbox.get(1.0, tk.END))
        with open(file_path, 'w') as file:
            file.write(html_output)

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

root = tk.Tk()
root.title("Markdown to HTML Converter")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

open_button = tk.Button(frame, text="Open Markdown File", command=open_file)
open_button.pack(side=tk.LEFT)

save_button = tk.Button(frame, text="Save as HTML", command=save_file)
save_button.pack(side=tk.LEFT)

markdown_textbox = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
markdown_textbox.pack(padx=10, pady=10)

root.mainloop()
