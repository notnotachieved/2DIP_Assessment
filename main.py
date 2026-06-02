# Good morning, afternoon, evening guys, im the developer of this pice of code of my app even if you don't want to hear this nonsense. :)
# This is the main pice of code of my app, its the login and user info database part.
# I'm too lazy to write notes for my code. Thank you for understanding. :)
import tkinter as tk # Using tkinter for UI display
from tkinter import messagebox
import hashlib # Using this for SHA256 encrypting
import secrets # Using this for random salt deneration
import json # Using this for saving users' information
import os # Using this to check if the json file exists in PC
import hmac # Using this for secure hash comprsion
DB_FILE = "users_data.json"
MIN_PASS_LEN = 8 # Minimum password length
MAX_PASS_LEN = 32 # Maximum password length
def compute_safe_hash(password, salt):
    payload = (password + salt).encode('utf-8') # Adding salt to help prevent dictionary and rainbow table attacks.
    return hashlib.sha256(payload).hexdigest()
def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError: # If JSON file is corrupted, return empty database
                return {}
    return {}
def save_data(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("unsafe lgin system ")
        self.root.geometry("500x400") # Window size
        tk.Label(root, text="User Name:").pack(pady=5)
        self.ent_user = tk.Entry(root)
        self.ent_user.pack()
        tk.Label(root, text="Password:").pack(pady=5)
        self.ent_pass = tk.Entry(root, show="*") # Hide users password
        self.ent_pass.pack()
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Sign in", command=self.handle_login, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Sign up", command=self.handle_register, width=10).pack(side=tk.LEFT, padx=5)
    def handle_register(self):
        username = self.ent_user.get().strip()
        password = self.ent_pass.get()
        data = load_data()
        if not username or not password:
            messagebox.showwarning("Error_ID1_PW1", "User name and password required.")
            return
        if username in data:
            messagebox.showerror("Error_ID2", "The user name has been taken")
            return
        if not (MIN_PASS_LEN <= len(password) <= MAX_PASS_LEN):
            messagebox.showwarning("Error_PW_2", f"The password must be {MIN_PASS_LEN}-{MAX_PASS_LEN} .")
            return
        salt = secrets.token_hex(16) # Generate random salt
        pwd_hash = compute_safe_hash(password, salt)
        data[username] = {"salt": salt, "hash": pwd_hash}
        save_data(data)
        messagebox.showinfo("Success", "Your account have been created !")
    def handle_login(self):
        username = self.ent_user.get().strip()
        password = self.ent_pass.get()
        data = load_data()
        if username not in data:
            messagebox.showerror("Error_PWoID_3", "Invalid user name or password.") # Ensure privacy and security, making it impossible for attackers to verify the existence of the account.
            return
        if len(password) > 128:
            messagebox.showerror("Error_PWoID_4", "Invalid input, over limit.")
            return
        stored_salt = data[username]['salt']
        stored_hash = data[username]['hash']
        current_hash = compute_safe_hash(password, stored_salt)
        if hmac.compare_digest(current_hash, stored_hash):
            messagebox.showinfo("Success", f"Welcome，{username}！")
        else:
            messagebox.showerror("Error_PWoID2", "Invalid user name or password") # Ensure privacy and security, making it impossible for attackers to verify the existence of the account.
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
