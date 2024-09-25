from tkinter import messagebox

def confirm(title: str, message: str) -> bool:
    # response = messagebox.askyesnocancel(title, message)
    response = messagebox.showwarning(title,message)
    if response is None:
        # User clicked "Cancel"
        return False
    elif response:
        # User clicked "Yes"  
        return True

def alert(title: str, message: str) -> bool:
    messagebox.showwarning(title,message)