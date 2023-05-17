import tkinter as tk
from tkinter import messagebox
from Password_Generator import Password
import json


class PasswordManager:
    def __init__(self, win):
        self.window = win
        self.window.geometry("600x400")
        self.window.configure(background="white")
        self.window.title("Your Female Password Manager")

        ##chika image
        self.canvas = tk.Canvas(height=100, width=75, background="white")
        self.chika = tk.PhotoImage(file="chika_as_manager.gif")
        self.canvas.create_image(40, 53, image=self.chika)
        self.canvas.place(x=270, y=70)

        ##email,pw and platform label
        email_label = tk.Label(self.window, background="white", text="Email", font=("Aerial", 12), padx=2, pady=2)
        email_label.place(x=160, y=195)
        password_label = tk.Label(self.window, background="white", text="Password", font=("Aerial", 12), padx=2, pady=2)
        password_label.place(x=160, y=230)
        platform_label = tk.Label(self.window, background="white", text="Platform", font=("Aerial", 12), padx=2, pady=2)
        platform_label.place(x=160, y=265)

        ##entries
        self.email_entry = tk.Entry(self.window, width=30, borderwidth=3)
        self.email_entry.place(x=260, y=200)

        self.pw_entry = tk.Entry(self.window, width=30, borderwidth=3)
        self.pw_entry.place(x=260, y=235)

        self.plat_entry = tk.Entry(self.window, width=30, borderwidth=3)
        self.plat_entry.place(x=260, y=270)

        ##buttons
        self.generate_button = tk.Button(self.window, text="Generate", command=self.random_password)
        self.generate_button.place(x=450, y=231)
        self.save_button = tk.Button(self.window, text="Save", command=self.save_password)
        self.save_button.place(x=280, y=320)

    def empty_entries(self):
        return not self.email_entry.get().strip() or not self.pw_entry.get().strip() \
            or not self.plat_entry.get().strip()

    def random_password(self):
        self.pw_entry.delete(0, tk.END)
        p = Password()
        self.pw_entry.insert(0, f"{p.generate_password()}")

    def save_password(self):
        if self.empty_entries():
            messagebox.showwarning("Fill me up", "Please don't leave me empty")
        else:
            email, password, platform = self.email_entry.get(), self.pw_entry.get(), self.plat_entry.get()
            user_data = self.read_json()
            new_user = True
            if platform in user_data and user_data[platform]["email"] == email:
                result = messagebox.askyesno("You have a saved password", "Update the password?")
                if result:
                    user_data[platform]["password"] = password
                    new_user = False
                else:
                    self.pw_entry.delete(0, tk.END)
                    pw = user_data[platform]["password"]
                    self.pw_entry.insert(0, f"{pw}")
            elif platform not in user_data:
                user_data[platform] = {f"email : {email}, password : {password}"}
            if new_user:
                new_data = {f"{platform}": {"email": f"{email}", "password": f"{password}"}}
                user_data.update(new_data)
            self.write_json(user_data)
            messagebox.showinfo("Mwah", "Password Saved")

    def read_json(self):
        try:
            with open("User_data.json") as data:
                user_data = json.load(data)
        except FileNotFoundError:
            user_data = {}
        return user_data

    def write_json(self, user_data):
        with open("User_data.json", mode='w') as file:
            json.dump(user_data, file)


if __name__ == "__main__":
    window = tk.Tk()
    password_manager = PasswordManager(window)
    window.mainloop()
