import string
import random
from tkinter import *
from tkinter import messagebox
import sqlite3

# Database setup
with sqlite3.connect("users.db") as db:
    cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users(Username TEXT NOT NULL, GeneratedPassword TEXT NOT NULL);")
cursor.execute("SELECT * FROM users")
db.commit()
db.close()

class PasswordGeneratorApp:
    def __init__(self, master):
        self.master = master
        self.username = StringVar()
        self.passwordlen = IntVar()
        self.generatedpassword = StringVar()

        self.setup_ui()

    def setup_ui(self):
        self.master.title('Password Generator')
        self.master.geometry('600x400')
        self.master.config(bg='#FF8000')
        self.master.resizable(False, False)

        Label(self.master, text="PASSWORD GENERATOR", anchor=N, fg='darkblue', bg='#FF8000', font='Arial 20 bold underline').pack(pady=10)

        frame = Frame(self.master, bg='#FF8000')
        frame.pack(pady=10)

        Label(frame, text="Enter User Name:", font='Times 15 bold', bg='#FF8000', fg='darkblue').grid(row=0, column=0, pady=5, sticky=E)
        Entry(frame, textvariable=self.username, font='Times 15', bd=6, relief='ridge').grid(row=0, column=1, pady=5)

        Label(frame, text="Enter Password Length:", font='Times 15 bold', bg='#FF8000', fg='darkblue').grid(row=1, column=0, pady=5, sticky=E)
        Entry(frame, textvariable=self.passwordlen, font='Times 15', bd=6, relief='ridge').grid(row=1, column=1, pady=5)

        Label(frame, text="Generated Password:", font='Times 15 bold', bg='#FF8000', fg='darkblue').grid(row=2, column=0, pady=5, sticky=E)
        Entry(frame, textvariable=self.generatedpassword, font='Times 15', bd=6, relief='ridge', fg='#DC143C', state='readonly').grid(row=2, column=1, pady=5)

        button_frame = Frame(self.master, bg='#FF8000')
        button_frame.pack(pady=20)

        Button(button_frame, text="GENERATE PASSWORD", bd=3, relief='solid', padx=10, pady=5, font='Verdana 15 bold', fg='#68228B', bg='#BCEE68', command=self.generate_pass).grid(row=0, column=0, padx=10)
        Button(button_frame, text="ACCEPT", bd=3, relief='solid', padx=10, pady=5, font='Helvetica 15 bold italic', fg='#458B00', bg='#FFFAF0', command=self.accept_fields).grid(row=0, column=1, padx=10)
        Button(button_frame, text="RESET", bd=3, relief='solid', padx=10, pady=5, font='Helvetica 15 bold italic', fg='#458B00', bg='#FFFAF0', command=self.reset_fields).grid(row=0, column=2, padx=10)

    def generate_pass(self):
        upper = string.ascii_uppercase
        lower = string.ascii_lowercase
        chars = "@#%&()\"?!"
        numbers = string.digits

        name = self.username.get()
        leng = self.passwordlen.get()

        if not name:
            messagebox.showerror("Error", "Name cannot be empty")
            return

        if not name.isalpha():
            messagebox.showerror("Error", "Name must be a string")
            self.username.set("")
            return

        if not isinstance(leng, int) or leng < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            self.passwordlen.set(0)
            return

        self.generatedpassword.set('')

        u = random.randint(1, leng - 3)
        l = random.randint(1, leng - 2 - u)
        c = random.randint(1, leng - 1 - u - l)
        n = leng - u - l - c

        password = random.sample(upper, u) + random.sample(lower, l) + random.sample(chars, c) + random.sample(numbers, n)
        random.shuffle(password)
        self.generatedpassword.set("".join(password))

    def accept_fields(self):
        with sqlite3.connect("users.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE Username = ?", (self.username.get(),))
            if cursor.fetchall():
                messagebox.showerror("Error", "This username already exists! Please use another username")
            else:
                cursor.execute("INSERT INTO users (Username, GeneratedPassword) VALUES (?, ?)", (self.username.get(), self.generatedpassword.get()))
                db.commit()
                messagebox.showinfo("Success!", "Password generated successfully")

    def reset_fields(self):
        self.username.set("")
        self.passwordlen.set(0)
        self.generatedpassword.set("")

if __name__ == '__main__':
    root = Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
