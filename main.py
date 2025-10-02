import tkinter as tk
from tkinter import ttk, messagebox
import json
import admin
import kasir   # panggil class KasirApp

USER_FILE = "users.json"

def load_users():
    with open(USER_FILE, "r") as f:
        return json.load(f)

def login():
    username = entry_user.get().strip()
    password = entry_pass.get().strip()
    users = load_users()

    for u in users:
        if u["username"] == username and u["password"] == password:
            login_window.destroy()
            if u["role"] == "admin":
                admin.admin_panel()
            elif u["role"] == "kasir":
                root = tk.Tk()
                kasir.KasirApp(root)
                root.mainloop()
            return
    messagebox.showerror("Login Gagal", "Username/password salah!")

# === LOGIN UI ===
login_window = tk.Tk()
login_window.title("Login System")
login_window.geometry("320x200")
login_window.configure(bg="#f8f9fa")

tk.Label(login_window, text="🔑 Login", font=("Segoe UI", 14, "bold"), bg="#f8f9fa").pack(pady=15)

frame = tk.Frame(login_window, bg="#f8f9fa")
frame.pack()

tk.Label(frame, text="Username:", bg="#f8f9fa").grid(row=0, column=0, padx=5, pady=5)
entry_user = ttk.Entry(frame, width=25)
entry_user.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Password:", bg="#f8f9fa").grid(row=1, column=0, padx=5, pady=5)
entry_pass = ttk.Entry(frame, show="*", width=25)
entry_pass.grid(row=1, column=1, padx=5, pady=5)

ttk.Button(login_window, text="Login", command=login).pack(pady=15)

login_window.mainloop()
