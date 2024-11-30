import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import subprocess
from tkinter import ttk
import keyword
import re

class SypherLangIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("SypherLang IDE")
        self.root.geometry("1000x700")
        self.create_widgets()
        self.filename = None

    def create_widgets(self):
        # Create Menu
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        run_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Run", menu=run_menu)
        run_menu.add_command(label="Run File", command=self.run_file)

        # Create Toolbar
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.syntax_highlight_button = ttk.Button(toolbar, text="Syntax Highlight", command=self.syntax_highlight)
        self.syntax_highlight_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.autocomplete_button = ttk.Button(toolbar, text="Autocomplete", command=self.autocomplete)
        self.autocomplete_button.pack(side=tk.LEFT, padx=2, pady=2)

        # Create Editor
        self.editor = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, undo=True, font=("Courier New", 12))
        self.editor.pack(fill=tk.BOTH, expand=1)
        self.editor.bind('<KeyRelease>', self.on_key_release)

        # Create Console
        self.console = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=10, state='disabled', font=("Courier New", 12), bg='black', fg='white')
        self.console.pack(fill=tk.X)

    def new_file(self):
        self.filename = None
        self.editor.delete(1.0, tk.END)

    def open_file(self):
        self.filename = filedialog.askopenfilename(defaultextension=".sypher", filetypes=[("SypherLang Files", "*.sypher"), ("All Files", "*.*")])
        if self.filename:
            with open(self.filename, "r") as f:
                self.editor.delete(1.0, tk.END)
                self.editor.insert(tk.INSERT, f.read())

    def save_file(self):
        if self.filename:
            with open(self.filename, "w") as f:
                f.write(self.editor.get(1.0, tk.END))
        else:
            self.save_as()

    def save_as(self):
        self.filename = filedialog.asksaveasfilename(defaultextension=".sypher", filetypes=[("SypherLang Files", "*.sypher"), ("All Files", "*.*")])
        if self.filename:
            self.save_file()

    def run_file(self):
        if not self.filename:
            messagebox.showerror("Error", "Please save your file before running.")
            return
        self.save_file()
        command = ["python", "interpreter.py", self.filename]
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
        except subprocess.CalledProcessError as e:
            output = e.output

        self.console.configure(state='normal')
        self.console.delete(1.0, tk.END)
        self.console.insert(tk.INSERT, output)
        self.console.configure(state='disabled')

    def syntax_highlight(self):
        """
        Highlight SypherLang keywords in the editor.
        """
        self.editor.tag_remove("keyword", "1.0", tk.END)
        words = r'\b(' + '|'.join(keyword.kwlist + ["function", "let", "encrypt", "prove_privacy", "execute_parallel"]) + r')\b'
        matches = re.finditer(words, self.editor.get(1.0, tk.END))

        for match in matches:
            start_idx = f"1.0 + {match.start()} chars"
            end_idx = f"1.0 + {match.end()} chars"
            self.editor.tag_add("keyword", start_idx, end_idx)

        self.editor.tag_config("keyword", foreground="blue", font=("Courier New", 12, "bold"))

    def on_key_release(self, event=None):
        """
        Highlight syntax after key release.
        """
        self.syntax_highlight()

    def autocomplete(self):
        """
        Provide simple autocompletion for common SypherLang functions and keywords.
        """
        cursor_position = self.editor.index(tk.INSERT)
        line_content = self.editor.get(f"{cursor_position} linestart", cursor_position)
        tokens = ["function", "let", "encrypt", "decrypt", "prove_privacy", "execute_parallel", "zkp_verify", "parallel_exec", "quantum_safe"]

        for token in tokens:
            if line_content.endswith(token[:3]):
                self.editor.insert(tk.INSERT, token[3:])
                return

    def autocomplete_suggestions(self, event=None):
        """
        Suggest possible completions based on current text input.
        """
        cursor_index = self.editor.index(tk.INSERT)
        current_line = self.editor.get(f"{cursor_index} linestart", cursor_index)
        possible_completions = [kw for kw in keyword.kwlist if current_line.strip() in kw]
        if possible_completions:
            self.console.configure(state='normal')
            self.console.insert(tk.END, "\nSuggestions: " + ', '.join(possible_completions))
            self.console.configure(state='disabled')

    def find_and_replace(self):
        """
        Launch a simple find and replace utility.
        """
        find_window = tk.Toplevel(self.root)
        find_window.title("Find and Replace")

        tk.Label(find_window, text="Find:").grid(row=0, column=0, padx=4, pady=4)
        tk.Label(find_window, text="Replace:").grid(row=1, column=0, padx=4, pady=4)

        find_entry = tk.Entry(find_window)
        replace_entry = tk.Entry(find_window)

        find_entry.grid(row=0, column=1, padx=4, pady=4)
        replace_entry.grid(row=1, column=1, padx=4, pady=4)

        def replace_text():
            find_text = find_entry.get()
            replace_text = replace_entry.get()
            content = self.editor.get(1.0, tk.END)
            new_content = content.replace(find_text, replace_text)
            self.editor.delete(1.0, tk.END)
            self.editor.insert(1.0, new_content)

        replace_button = tk.Button(find_window, text="Replace All", command=replace_text)
        replace_button.grid(row=2, column=1, sticky=tk.W, padx=4, pady=4)

if __name__ == "__main__":
    root = tk.Tk()
    ide = SypherLangIDE(root)
    root.mainloop()
