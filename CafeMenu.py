import hashlib # Using this for SHA256 encrypting.
import secrets # Using this for random salt generation.
import json # Using this for saving users' information.
import os # Using this to check if the json file exists in PC.
import hmac # Using this for secure hash comprsion.
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
def register():
    print("\n=== SIGN UP ===")
    username = input("Create username: ").strip() # Remove leading and trailing whitespace from the username.
    password = input("Create password: ")
    data = load_data()
    if not username or not password:
        print("Username and password required.")
        return
    if username in data:
        print("Username already exists.")
        return
    if not (MIN_PASS_LEN <= len(password) <= MAX_PASS_LEN): # Validate password length.
        print(
            f"Password must be between "
            f"{MIN_PASS_LEN} and {MAX_PASS_LEN} characters."
        )
        return
    salt = secrets.token_hex(16) # Generate random salt (32 characters hex string).
    password_hash = compute_safe_hash(
        password,
        salt
    )
    data[username] = {
        "salt": salt,
        "hash": password_hash
    }
    save_data(data)
    print("Account created successfully.")
def login():
    print("\n=== SIGN IN ===")
    username = input("Username: ").strip()
    password = input("Password: ")
    data = load_data()
    if username not in data:
        print("Invalid username or password.")
        return None
    if len(password) > 128:
        print("Invalid input.")
        return None
    stored_salt = data[username]["salt"]
    stored_hash = data[username]["hash"]
    current_hash = compute_safe_hash(
        password,
        stored_salt
    )
    if hmac.compare_digest(
        current_hash,
        stored_hash
    ):
        print(f"\nWelcome, {username}!")
        return username
    print("Invalid username or password.")
    return None
def display_menu():
    print("\n===================")
    print("     CAFE MENU")
    print("===================")
    for item_id, (name, price) in PRODUCTS.items():
        print(
            f"{item_id}. " # Format the item ID, name, and price, and format price to 2 decimal places.
            f"{name:<10}" # Left-align item name within 10 characters.
            f"${price:.2f}" # Format price to 2 decimal places and left-align it within 10 characters.
        )
def place_order(username):
    order = []
    total = 0
    while True:
        display_menu()
        choice = input(
            "\nSelect item number " # Prompt the user to select an item.
            "(0 to finish): " 
        )
        if choice == "0":
            break
        if not choice.isdigit(): # Validate that the input is a number..
            print("Invalid input.")
            continue
        choice = int(choice)
        if choice not in PRODUCTS:
            print("Item not found.")
            continue
        quantity = input("Quantity: ")
        if not quantity.isdigit() or int(quantity) <= 0:
            print("Invalid quantity.")
            continue
        quantity = int(quantity)
        item_name, item_price = PRODUCTS[choice]
        subtotal = item_price * quantity
        order.append(
            (
                item_name,
                quantity,
                item_price,
                subtotal
            )
        )
        total += subtotal
        print(
            f"Added {quantity} x " # Format the item name and quantity, and format price to 2 decimal places.
            f"{item_name}"
        )
    if len(order) == 0:
        print("No items ordered.")
        return
    generate_invoice(
        username,
        order,
        total
    )
def generate_invoice(
    username,
    order,
    total
):
    order_id = secrets.token_hex(4).upper() # Generate a random order ID (8 characters hex string).
    print("\n")
    print("=" * 40)
    print("            INVOICE")
    print("=" * 40)
    print(f"Order ID : {order_id}")
    print(f"Customer : {username}")
    print("\nItems")
    print("-" * 40)
    for item_name, qty, price, subtotal in order:
        print(
            f"{item_name:<10}" # Left-align item name within 10 characters.
            f"x{qty:<3}" # Left-align item name and quantity, and format price and subtotal to 2 decimal places.
            f"${price:<6.2f}" # Format price to 2 decimal places and left-align it within 6 characters.
            f"${subtotal:.2f}" # Format subtotal to 2 decimal places.
        )
    print("-" * 40) # Print a separator line.
    print(f"TOTAL: ${total:.2f}") # Format total to 2 decimal places.
    print("=" * 40) # Print a separator line.
    save_invoice(
        username,
        order_id,
        order,
        total
    )
def save_invoice(
    username,
    order_id,
    order,
    total
):
    filename = (
        f"invoice_"
        f"{username}_" 
        f"{order_id}.txt" 
    )
    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(
            "SCHOOL CAFE INVOICE\n" # Write the header of the invoice.
        )
        f.write(
            "=" * 30 + "\n" # Print a separator line.
        )
        f.write(
            f"Order ID: "
            f"{order_id}\n" # Write order ID to the invoice.
        )
        f.write(
            f"Customer: "
            f"{username}\n\n" # Add an extra newline for better formatting.
        )
        for item_name, qty, price, subtotal in order:
            f.write(
                f"{item_name} " # Format item name, and format price and subtotal to 2 decimal places.
                f"x{qty} " # Format item name and quantity, and format price and subtotal to 2 decimal places.
                f"${subtotal:.2f}\n" # Format subtotal to 2 decimal places.
            )
        f.write(
            "\nTOTAL: "
            f"${total:.2f}\n" # Format total to 2 decimal places.
        )
    print(
        f"Invoice saved as "
        f"'{filename}'"
    )
def user_menu(username):
    while True:
        print("\n")
        print("===================")
        print("     USER MENU")
        print("===================")
        print("1. View Menu")
        print("2. Place Order")
        print("3. Logout")
        choice = input(
            "\nEnter choice: " # Prompt the user to select an option from the user menu.
        )
        if choice == "1":
            display_menu()
        elif choice == "2":
            place_order(username)
        elif choice == "3":
            print("Logged out.")
            break
        else:
            print("Invalid option.")
def main():
    while True:
        print("\n")
        print("==============================")
        print(" SCHOOL CAFE CLICK & COLLECT ")
        print("==============================")
        print("1. Sign Up")
        print("2. Sign In")
        print("3. Exit")
        choice = input(
            "\nSelect option: "
        )
        if choice == "1":
            register()
        elif choice == "2":
            user = login()
            if user:
                user_menu(user)
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")
main()
