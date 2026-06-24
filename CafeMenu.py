import hashlib # Using this for SHA256 encrypting.
import secrets # Using this for random salt generation.
import hmac # Using this for secure hash comprsion.
import json # Using this for saving users' information.
import os # Using this to check if the json file exists in PC.
import tkinter as tk # Using this for GUI.
from tkinter import messagebox # Using this for showing message boxes in GUI.

DB_FILE = "users_data.json" # User database file.
MIN_PASS_LEN = 8 # Minimum password length.
MAX_PASS_LEN = 32 # Maximum password length. 
PRODUCTS = {
    1: ("Pie", 4.50),
    2: ("Sandwich", 5.00),
    3: ("Muffin", 3.00),
    4: ("Juice", 2.50),
    5: ("Coffee", 4.00)
    }

###################UI####################
root = tk.Tk()
root.geometry("600x500") # Window size
current_order = [] # Store the current order items
current_total = 0.0 # Store the current order total

def clear_window():
    for widget in root.winfo_children(): # Loop through all widgets in the window and destroy them to clear the window for the next screen.
        widget.destroy()

def compute_safe_hash(password, salt):
    payload = (password + salt).encode("utf-8") # Adding salt to help prevent dictionary and rainbow table attacks.
    return hashlib.sha256(payload).hexdigest() # Return the hash value as a hexadecimal string.

def load_data():
    if os.path.exists(DB_FILE): # Check if the JSON file exists in the current directory.
        with open(DB_FILE, "r", encoding="utf-8") as f: # Open the JSON file in read mode with UTF-8 encoding.
            try:
                return json.load(f)
            except json.JSONDecodeError: # If JSON file is corrupted, return empty database.
                return {}
    return {}

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f: # Open the JSON file in write mode with UTF-8 encoding.
        json.dump(data, f, indent=4)

def handle_register(ent_user, ent_pass):
    username = ent_user.get().strip()
    password = ent_pass.get()
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

def handle_login(ent_user, ent_pass):
    username = ent_user.get().strip()
    password = ent_pass.get()
    data = load_data()
    if username not in data:
        messagebox.showerror("Error_PWoID_3", "Invalid user name or password.") # Ensure privacy and security
        return
    if len(password) > 128:
        messagebox.showerror("Error_PWoID_4", "Invalid input, over limit.")
        return
    stored_salt = data[username]['salt'] 
    stored_hash = data[username]['hash']
    current_hash = compute_safe_hash(password, stored_salt)
    if hmac.compare_digest(current_hash, stored_hash):
        messagebox.showinfo("Success", f"Welcome，{username}！")
        user_menu(username) 
    else:
        messagebox.showerror("Error_PWoID2", "Invalid user name or password") # Ensure privacy and security

def show_menu():
    clear_window()
    root.title("unsafe lgin system ")
    tk.Label(root, text="User Name:").pack(pady=5)
    ent_user = tk.Entry(root)
    ent_user.pack()
    tk.Label(root, text="Password:").pack(pady=5)
    self_ent_pass = tk.Entry(root, show="*") # Hide users password
    self_ent_pass.pack()
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=20)
    tk.Button(btn_frame, text="Sign in", command=lambda: handle_login(ent_user, self_ent_pass), width=10).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Sign up", command=lambda: handle_register(ent_user, self_ent_pass), width=10).pack(side=tk.LEFT, padx=5)
    tk.Button(root, text="Exit", command=root.quit, width=10, bg="#ffcccb").pack(pady=10)

def display_menu(parent_frame):
    for item_id, (name, price) in PRODUCTS.items():
        f = tk.Frame(parent_frame)
        f.pack(fill=tk.X, pady=4, padx=5)
        tk.Label(f, text=f"{item_id}. {name:<10} ${price:.2f}", font=("Courier", 11)).pack(side=tk.LEFT)

def place_order(username):
    clear_window()
    root.title(" Place Order ")
    global current_order, current_total
    current_order = [] 
    current_total = 0   
    tk.Label(root, text=f"=== PLACE ORDER ({username}) ===", font=("Arial", 12, "bold"), pady=10).pack()  
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10)
    left_frame = tk.LabelFrame(main_frame, text=" Cafe Menu ")
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    for item_id, (name, price) in PRODUCTS.items():
        f = tk.Frame(left_frame)
        f.pack(fill=tk.X, pady=5, padx=5)
        tk.Label(f, text=f"{name} (${price:.2f})", font=("Arial", 10)).pack(side=tk.LEFT)
        spin = tk.Spinbox(f, from_=1, to=20, width=3)
        spin.pack(side=tk.RIGHT, padx=2)
        
        def add_item(n=name, p=price, s=spin):
            try:
                quantity = int(s.get())
                if quantity <= 0: raise ValueError
            except ValueError:
                messagebox.showwarning("Invalid", "Invalid quantity.")
                return
            subtotal = p * quantity
            current_order.append((n, quantity, p, subtotal))
            global current_total
            current_total += subtotal
            update_cart_preview()
        tk.Button(f, text="Add", command=add_item, width=5).pack(side=tk.RIGHT)
    right_frame = tk.LabelFrame(main_frame, text=" Current Cart ")
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)  
    txt_preview = tk.Text(right_frame, width=25, height=12, font=("Courier", 10))
    txt_preview.pack(pady=5, padx=5)
    
    def update_cart_preview():
        txt_preview.config(state=tk.NORMAL)
        txt_preview.delete("1.0", tk.END)
        if not current_order:
            txt_preview.insert(tk.END, "No items ordered.")
        else:
            for item_name, qty, _, sub in current_order:
                txt_preview.insert(tk.END, f"{item_name:<10} x{qty:<2} ${sub:.2f}\n")
            txt_preview.insert(tk.END, f"\nTotal: ${current_total:.2f}")
        txt_preview.config(state=tk.DISABLED)
    update_cart_preview()

    def finish_order():
        if len(current_order) == 0:
            messagebox.showwarning("Empty", "No items ordered.")
            return
        generate_invoice(username, current_order, current_total)
        user_menu(username)
        
    tk.Button(root, text="Finish Order (0)", command=finish_order, bg="#ffa500", font=("Arial", 11)).pack(pady=10)
    tk.Button(root, text="Cancel", command=lambda: user_menu(username)).pack()

def generate_invoice(username, order, total):
    order_id = secrets.token_hex(4).upper()
    invoice_msg = "=" * 40 + "\n            INVOICE\n" + "=" * 40 + "\n"
    invoice_msg += f"Order ID : {order_id}\nCustomer : {username}\n\nItems\n" + "-" * 40 + "\n"
    for item_name, qty, price, subtotal in order:
        invoice_msg += f"{item_name:<10}x{qty:<3}${price:<6.2f}${subtotal:.2f}\n"
    invoice_msg += "-" * 40 + "\n" + f"TOTAL: ${total:.2f}\n" + "=" * 40 + "\n"
    
    messagebox.showinfo("Invoice", invoice_msg)
    save_invoice(username, order_id, order, total)

def save_invoice(username, order_id, order, current_total):
    filename = f"invoice_{username}_{order_id}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("SCHOOL CAFE INVOICE\n") # Write the header of the invoice.
        f.write("=" * 30 + "\n") # Print a separator line.
        f.write(f"Order ID: {order_id}\n") # Write order ID to the invoice.
        f.write(f"Customer: {username}\n\n") # Add an extra newline for better formatting.
        for item_name, qty, price, subtotal in order: # Write each item in the order to the invoice, showing the item name, quantity, and subtotal for that item.
            f.write(f"{item_name} x{qty} ${subtotal:.2f}\n") # Write each item in the order to the invoice, showing the item name, quantity, and subtotal for that item.
        f.write(f"\nTOTAL: ${current_total:.2f}\n") # Add an extra newline before the total for better formatting.
    messagebox.showinfo("Saved", f"Invoice saved as '{filename}'")

def user_menu(username):
    clear_window()
    root.title("School Cafe - User Menu")   
    tk.Label(root, text="===================", fg="gray").pack()
    tk.Label(root, text="     USER MENU", font=("Arial", 14, "bold")).pack()
    tk.Label(root, text="===================", fg="gray").pack()
    menu_view_frame = tk.Frame(root)
    
    def toggle_menu_view():
        if menu_view_frame.winfo_children():
            for w in menu_view_frame.winfo_children(): w.destroy()
            menu_view_frame.pack_forget()
        else:
            menu_view_frame.pack(pady=5)
            display_menu(menu_view_frame)
    tk.Button(root, text="1. View Menu", font=("Arial", 11), width=20, command=toggle_menu_view).pack(pady=5)
    tk.Button(root, text="2. Place Order", font=("Arial", 11), width=20, command=lambda: place_order(username)).pack(pady=5)
    tk.Button(root, text="3. Logout", font=("Arial", 11), width=20, fg="red", command=show_menu).pack(pady=5) # 修正：show_auth_menu -> show_menu

def main():
    show_menu()
if __name__ == "__main__":
    main()
    root.mainloop()