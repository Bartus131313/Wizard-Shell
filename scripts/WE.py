import tkinter as tk
from tkinter import filedialog
import os
import sys
import importlib
import re

TEXT_TAGS = [
    # PURPLE
    {'import' : '#bf00ff'}, 
    {'if' : '#bf00ff'}, 
    {'while' : '#bf00ff'}, 
    {'from' : '#bf00ff'}, 
    {'as' : '#bf00ff'}, 
    # BLUE
    {'def': '#0099ff'},
    # YELLOW
    {'print' : '#ffff00'}
]

TEXT_TAGS_AFTER = [
    {True : '#00ffbf'},
    {True : '#00bfff'},
    {True : '#00bfff'},
    {True : '#00ffbf'},
    {True : '#00ffbf'},
    {True : '#ffff00'},
    {False: ''}
]

SCRIPT_RUN = False

SCRIPTS_DIR = os.path.dirname(__file__)

WIZARD_SHELL_DIR = os.path.dirname(SCRIPTS_DIR)

sys.path.append(WIZARD_SHELL_DIR)

ws = importlib.import_module('main')

def insert_spaces(event):
    editor.insert(tk.INSERT, " " * 3)
    return "break"  # Prevent the default tab behavior

def handle_parenthesis(event):
    if event.char == "(":
        editor.insert(tk.INSERT, "()")
        editor.mark_set(tk.INSERT, f"{tk.INSERT}-1c")  # Move cursor inside parentheses
        return "break"  # Prevent the default keypress behavior
    if event.char == "[":
        editor.insert(tk.INSERT, "[]")
        editor.mark_set(tk.INSERT, f"{tk.INSERT}-1c")  # Move cursor inside parentheses
        return "break"  # Prevent the default keypress behavior
    if event.char == "{":
        editor.insert(tk.INSERT, "{}")
        editor.mark_set(tk.INSERT, f"{tk.INSERT}-1c")  # Move cursor inside parentheses
        return "break"  # Prevent the default keypress behavior

def hsc(text):
    pattern = r'[^a-zA-Z0-9-_]'  # Regular expression pattern
    match = re.search(pattern, text)
    if match:
        return True  # String contains special characters
    else:
        return False  # String does not contain special characters

def apply_syntax_highlighting(event=None):
    i = 0
    # Clear existing tags
    all_tags = editor.tag_names()
    for tag in all_tags:
        editor.tag_delete(tag)
    
    # Find and apply tags for specific words
    try:
        for item in TEXT_TAGS:
            for tag, col in item.items():
                start = "1.0"
                while True:
                    start = editor.search(tag, start, tk.END)
                    if not start:
                        break
                    end = f"{start}+{len(tag)}c"
                    editor.tag_add(tag, start, end)
                    editor.tag_configure(tag, foreground=col)
                    start = end

                    for en, color in TEXT_TAGS_AFTER[i].items():
                        if en:
                            end = editor.search(r'\s', start, tk.END, regexp=True)
                            text_after = editor.get(end, f"{end}+512c")
                            if text_after.strip():
                                txt = text_after.split()[0]
                                if not hsc(txt):
                                    start = editor.search(txt, start, tk.END)
                                    end = f"{start}+{len(txt)}c"
                                    editor.tag_add(txt, start, end)
                                    editor.tag_configure(txt, foreground=color)
                                else:
                                    cls_txt = re.sub(r'[^a-zA-Z0-9-_ ]', '', txt)
                                    start = editor.search(cls_txt, start, tk.END)
                                    end = f"{start}+{len(cls_txt)}c"
                                    editor.tag_add(cls_txt, start, end)
                                    editor.tag_configure(cls_txt, foreground=color)

                            if not end:
                                end = tk.END

                i += 1
    except:
        print('ERROR')

def open_file(event=None):
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as file:
            editor.delete('1.0', 'end')
            editor.insert('1.0', file.read())

    update_lines()
    apply_syntax_highlighting()

def save_file(event=None):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=(("Python files", "*.py"),),
                                             initialdir=SCRIPTS_DIR)
    if file_path:
        with open(file_path, 'w') as file:
            file.write(editor.get('1.0', 'end'))

def on_scroll2(event=None):
    line_numbers.yview_moveto(editor.yview()[0])

def update_line_numbers(event):
    line_numbers.configure(state="normal")
    line_numbers.delete('1.0', 'end')

    def delayed_update():
        line_count = int(editor.index('end-1c').split('.')[0])
        line_numbers_text = "\n".join(str(i) for i in range(1, line_count + 1))
        line_numbers.insert(tk.END, line_numbers_text)
        line_numbers.configure(state="disabled")

        if line_count >= 50:
            line_numbers.yview_moveto(editor.yview()[0])

    line_numbers.after(1, delayed_update)

def update_lines():
    line_numbers.configure(state="normal")
    line_numbers.delete('1.0', 'end')

    line_count = int(editor.index('end-1c').split('.')[0])
    line_numbers_text = "\n".join(str(i) for i in range(1, line_count + 1))
    line_numbers.insert(tk.END, line_numbers_text)
    line_numbers.configure(state="disabled")

def on_scroll(*args):
    line_numbers.yview(*args)
    editor.yview(*args)

def SCRIPT():

    global SCRIPT_RUN

    if SCRIPT_RUN:

        SCRIPT_RUN = False

        global editor
        global line_numbers

        root = tk.Tk()
        root.title("WE | Wizard Editor 0.0.0.1")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x = int((screen_width - 1200) / 2)
        y = int((screen_height - 800) / 2)

        root.geometry("1200x800+{}+{}".format(x, y))

        line_numbers = tk.Text(root, width=4, padx=4, takefocus=0, border=0)
        line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        line_numbers.configure(bg="#141414", fg="white", state="disabled")

        scrollbar = tk.Scrollbar(root)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        editor = tk.Text(root, insertbackground='red', yscrollcommand=scrollbar.set, border=0)
        editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=on_scroll)

        editor.bind('<Key>', update_line_numbers)
        editor.bind('<KeyRelease>', apply_syntax_highlighting)
        editor.bind("<Tab>", insert_spaces)
        editor.bind("<KeyPress>", handle_parenthesis)
        editor.configure(bg="#232323", fg="white")


        menubar = tk.Menu(root)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=open_file)
        filemenu.add_command(label="Save", command=save_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)

        menubar.add_cascade(label="File", menu=filemenu)

        root.config(menu=menubar)
        root.bind('<Control-s>', save_file)
        root.bind('<Control-o>', open_file)
        root.bind('<MouseWheel>', on_scroll2)

        update_lines()

        root.mainloop()

        ws.ws_return(False) # Return to Wizard Shell

# SCRIPT WORK

def main(cmd):
    if cmd == 'start':
        global SCRIPT_RUN
        SCRIPT_RUN = True
        SCRIPT()

def commands():
    return ['start']