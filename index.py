import tkinter as tk
import crawler as c

def log(message):
    print("pressed")
    txt_edit.config(state="normal")
    txt_edit.insert(tk.END, message)
    txt_edit.config(state="disabled")


window = tk.Tk()
window.title("Aniloader")
window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(2, minsize=800, weight=1)

txt_edit = tk.Text(window)
txt_edit.config(state="disabled")
fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
btn_open = tk.Button(fr_buttons, text="Open", command= lambda: c.update_seasonal())
btn_save = tk.Button(fr_buttons, text="Save As...")

btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5)


fr_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=2, sticky="nsew")

window.mainloop()

