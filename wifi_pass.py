import subprocess
from tkinter import *
import tkinter.messagebox as messagebox

def show_pass():
    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
    profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
    passwords = ""
    for i in profiles:
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').split('\n')
        results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
        try:
            passwords +=("{:<30}|  {:<}\n".format(i, results[0]))
        except IndexError:
            passwords +=("{:<30}|  {:<}\n".format(i, ""))
    return passwords

def update_text():
    passw = show_pass()
    text.delete("1.0", END)
    text.insert(END, passw)

def copy_password():
    password = text.get("1.0", END)
    root.clipboard_clear()
    root.clipboard_append(password)
    messagebox.showinfo("Password Copied", "Password has been copied to clipboard.")

def save_to_file():
    password = text.get("1.0", END)
    with open("passwords.txt", "w") as file:
        file.write(password)
    messagebox.showinfo("File Saved", "Passwords have been saved to passwords.txt.")

root = Tk()
root.title("Wifi Password Finder")

btn_show = Button(root, text="Show Passwords", command=update_text)
btn_show.pack()

text = Text(root, wrap=WORD, width=60, height=20)
text.pack()

# Add right-click context menu
popup_menu = Menu(root, tearoff=0)
popup_menu.add_command(label="Copy", command=copy_password)
popup_menu.add_command(label="Save to File", command=save_to_file)
text.bind("<Button-3>", lambda event: popup_menu.post(event.x_root, event.y_root))

root.mainloop()
