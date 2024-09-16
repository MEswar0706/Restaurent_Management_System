import tkinter as tk
from tkinter import messagebox, scrolledtext
import sqlite3

# Function to create and connect to the database
def create_db():
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    # Create tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to add an item to the inventory
def add_item():
    item_name = item_name_entry.get()
    quantity = quantity_entry.get()
    if item_name and quantity:
        try:
            quantity = int(quantity)
            conn = sqlite3.connect('restaurant.db')
            c = conn.cursor()
            c.execute('INSERT INTO inventory (item_name, quantity) VALUES (?, ?)', (item_name, quantity))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Item '{item_name}' added to inventory!")
            item_name_entry.delete(0, tk.END)
            quantity_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number")
    else:
        messagebox.showerror("Error", "Please fill in all fields")

# Function to place an order
def place_order():
    item_name = order_item_name_entry.get()
    quantity = order_quantity_entry.get()
    if item_name and quantity:
        try:
            quantity = int(quantity)
            conn = sqlite3.connect('restaurant.db')
            c = conn.cursor()
            # Check if enough inventory is available
            c.execute('SELECT quantity FROM inventory WHERE item_name = ?', (item_name,))
            result = c.fetchone()
            if result and result[0] >= quantity:
                c.execute('INSERT INTO orders (item_name, quantity) VALUES (?, ?)', (item_name, quantity))
                c.execute('UPDATE inventory SET quantity = quantity - ? WHERE item_name = ?', (quantity, item_name))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", f"Order for '{item_name}' placed successfully!")
            else:
                messagebox.showerror("Error", "Not enough inventory for this item")
            order_item_name_entry.delete(0, tk.END)
            order_quantity_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Error", "Please fill in all fields")

# Function to show inventory
def show_inventory():
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    c.execute('SELECT * FROM inventory')
    rows = c.fetchall()
    conn.close()

    inventory_window = tk.Toplevel(root)
    inventory_window.title("Inventory")

    text_area = scrolledtext.ScrolledText(inventory_window, width=50, height=20)
    text_area.pack(padx=10, pady=10)

    if rows:
        text_area.insert(tk.END, "Item ID | Item Name | Quantity\n")
        text_area.insert(tk.END, "-"*40 + "\n")
        for row in rows:
            text_area.insert(tk.END, f"{row[0]} | {row[1]} | {row[2]}\n")
    else:
        text_area.insert(tk.END, "No inventory items found")

# Function to show orders
def show_orders():
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    c.execute('SELECT * FROM orders')
    rows = c.fetchall()
    conn.close()

    orders_window = tk.Toplevel(root)
    orders_window.title("Orders")

    text_area = scrolledtext.ScrolledText(orders_window, width=50, height=20)
    text_area.pack(padx=10, pady=10)

    if rows:
        text_area.insert(tk.END, "Order ID | Item Name | Quantity\n")
        text_area.insert(tk.END, "-"*40 + "\n")
        for row in rows:
            text_area.insert(tk.END, f"{row[0]} | {row[1]} | {row[2]}\n")
    else:
        text_area.insert(tk.END, "No orders found")

# Create the database and tables
create_db()

# Create the main window
root = tk.Tk()
root.title("Restaurant Management System")

# Inventory Management
inventory_frame = tk.Frame(root)
inventory_frame.pack(padx=10, pady=10)

tk.Label(inventory_frame, text="Item Name:").grid(row=0, column=0, padx=5, pady=5)
item_name_entry = tk.Entry(inventory_frame)
item_name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(inventory_frame, text="Quantity:").grid(row=1, column=0, padx=5, pady=5)
quantity_entry = tk.Entry(inventory_frame)
quantity_entry.grid(row=1, column=1, padx=5, pady=5)

add_button = tk.Button(inventory_frame, text="Add Item", command=add_item)
add_button.grid(row=2, columnspan=2, pady=10)

# Order Management
order_frame = tk.Frame(root)
order_frame.pack(padx=10, pady=10)

tk.Label(order_frame, text="Order Item Name:").grid(row=0, column=0, padx=5, pady=5)
order_item_name_entry = tk.Entry(order_frame)
order_item_name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(order_frame, text="Order Quantity:").grid(row=1, column=0, padx=5, pady=5)
order_quantity_entry = tk.Entry(order_frame)
order_quantity_entry.grid(row=1, column=1, padx=5, pady=5)

place_order_button = tk.Button(order_frame, text="Place Order", command=place_order)
place_order_button.grid(row=2, columnspan=2, pady=10)

# Show Inventory and Orders
show_inventory_button = tk.Button(root, text="Show Inventory", command=show_inventory)
show_inventory_button.pack(padx=10, pady=5)

show_orders_button = tk.Button(root, text="Show Orders", command=show_orders)
show_orders_button.pack(padx=10, pady=5)

# Start the GUI event loop
root.mainloop()
