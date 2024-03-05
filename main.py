import tkinter as tk
from tkinter import scrolledtext, font
from contextlib import redirect_stdout
import io

def update_line_numbers(*args):
    line_numbers.delete("1.0", "end")
    i = '1.0'
    while True:
        dline = code_input.dlineinfo(i)
        if dline is None: break
        line_numbers.insert("end", str(i.split('.')[0]) + "\n")
        i = code_input.index(f"{i}+1line")
    line_numbers.config(state='disabled')

def on_scroll(*args):
    code_input.yview(*args)
    result_display.yview(*args)
    line_numbers.yview(*args)

def run_code():
    code_output = io.StringIO()
    with redirect_stdout(code_output):
        try:
            exec(code_input.get("1.0", tk.END))
            output = code_output.getvalue()
        except Exception as e:
            output = str(e)
    result_display.config(state=tk.NORMAL)
    result_display.delete("1.0", tk.END)
    result_display.insert(tk.INSERT, output)
    result_display.config(state=tk.DISABLED)
    code_output.close()

# Create the main window
root = tk.Tk()
root.title("Python Code Executor")

# Custom fonts
code_font = font.Font(family="Consolas", size=12)

# Frame for the code input and line numbers
frame1 = tk.Frame(root)
frame1.pack(fill=tk.BOTH, expand=True)

# Line number column
line_numbers = tk.Text(frame1, width=4, padx=3, takefocus=0, border=0,
                       background='gray', foreground='white', state='disabled')
line_numbers.pack(side=tk.LEFT, fill=tk.Y)

# Scrollbar
scrollbar = tk.Scrollbar(frame1)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Text widget for code input
code_input = scrolledtext.ScrolledText(frame1, height=15, width=50, font=code_font,
                                        yscrollcommand=scrollbar.set, wrap="none")
code_input.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
scrollbar.config(command=on_scroll)

# Frame for the output display
frame2 = tk.Frame(root)
frame2.pack(fill=tk.BOTH, expand=True)

# Text widget for output display
result_display = scrolledtext.ScrolledText(frame2, height=15, width=50, font=code_font,
                                           state=tk.DISABLED, wrap="none")
result_display.pack(fill=tk.BOTH, expand=True)

# "Run" button
run_button = tk.Button(root, text="Run", command=run_code)
run_button.pack(pady=10)

# Bind the event to update line numbers whenever the text changes or the user scrolls
code_input.bind("<KeyRelease>", lambda event: update_line_numbers())
code_input.bind("<MouseWheel>", lambda event: update_line_numbers())

# Initial call to populate line numbers
update_line_numbers()

root.mainloop()
