import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import datetime
import json
import os
import tempfile
import platform

# -------------------- Auth --------------------
users = {
    "sales": {"password": "sales123", "role": "sales"},
    "manager": {"password": "manager123", "role": "manager"}
}

# -------------------- Storage --------------------
INVENTORY_FILE = "inventory.json"
SALES_FILE = "sales.json"

def load_inventory():
    try:
        with open(INVENTORY_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_inventory(data):
    with open(INVENTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_sales():
    try:
        with open(SALES_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_sales(data):
    with open(SALES_FILE, "w") as f:
        json.dump(data, f, indent=4)

# -------------------- Inventory UI --------------------
def show_inventory_ui():
    for widget in root.winfo_children():
        widget.destroy()

    inv_frame = tk.Frame(root)
    inv_frame.pack(fill="both", expand=True, padx=12, pady=12)

    tk.Label(inv_frame, text="Inventory Management (Manager Only)", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)

    # Product Code
    tk.Label(inv_frame, text="Product Code").grid(row=1, column=0, sticky="w")
    code_entry = tk.Entry(inv_frame)
    code_entry.grid(row=1, column=1)

    # Product Type
    tk.Label(inv_frame, text="Product Type").grid(row=2, column=0, sticky="w")
    type_var = tk.StringVar()
    type_dropdown = ttk.Combobox(inv_frame, textvariable=type_var, values=["tops", "shirt", "pants", "shorts", "shoes", "fruits"], state="readonly")
    type_dropdown.grid(row=2, column=1)

    # Price
    tk.Label(inv_frame, text="Price").grid(row=3, column=0, sticky="w")
    price_entry = tk.Entry(inv_frame)
    price_entry.grid(row=3, column=1)

    # Date Added
    tk.Label(inv_frame, text="Date Added").grid(row=4, column=0, sticky="w")
    date_added = tk.Entry(inv_frame)
    date_added.insert(0, datetime.date.today().isoformat())
    date_added.grid(row=4, column=1)

    # Expiry Date
    tk.Label(inv_frame, text="Expiry Date (for fruits)").grid(row=5, column=0, sticky="w")
    expiry_entry = tk.Entry(inv_frame)
    expiry_entry.grid(row=5, column=1)

    # Max Discount
    tk.Label(inv_frame, text="Max Discount (%)").grid(row=6, column=0, sticky="w")
    discount_entry = tk.Entry(inv_frame)
    discount_entry.grid(row=6, column=1)

    def save_product():
        code = code_entry.get().strip()
        ptype = type_var.get().strip()
        price = price_entry.get().strip()
        date_val = date_added.get().strip()
        expiry = expiry_entry.get().strip()
        discount = discount_entry.get().strip()

        if not code or not ptype or not price or not date_val or not discount:
            messagebox.showerror("Error", "All fields except expiry (non-fruits) are required")
            return

        try:
            price = float(price)
            discount = int(discount)
        except ValueError:
            messagebox.showerror("Error", "Price must be a number and discount must be an integer")
            return

        if ptype == "fruits":
            if not expiry:
                messagebox.showerror("Error", "Expiry date is required for fruits")
                return
            try:
                datetime.date.fromisoformat(expiry)
            except ValueError:
                messagebox.showerror("Error", "Expiry date must be in YYYY-MM-DD format")
                return
        else:
            expiry = None

        inventory = load_inventory()
        for item in inventory:
            if item["code"] == code:
                messagebox.showerror("Error", "Product code already exists")
                return

        product = {
            "code": code,
            "type": ptype,
            "price": price,
            "date_added": date_val,
            "expiry_date": expiry,
            "max_discount": discount
        }

        inventory.append(product)
        save_inventory(inventory)
        messagebox.showinfo("Success", f"Product {code} added successfully")

        code_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        expiry_entry.delete(0, tk.END)
        discount_entry.delete(0, tk.END)
        type_var.set("")

    tk.Button(inv_frame, text="Save Product", command=save_product).grid(row=7, column=0, columnspan=2, pady=10)
    tk.Button(inv_frame, text="Go to Sales", command=show_sales_ui).grid(row=8, column=0, columnspan=2, pady=4)
    tk.Button(inv_frame, text="View Reports", command=show_reports_ui).grid(row=9, column=0, columnspan=2, pady=4)

# -------------------- Sales UI --------------------
def show_sales_ui():
    for widget in root.winfo_children():
        widget.destroy()

    sales_frame = tk.Frame(root)
    sales_frame.pack(fill="both", expand=True, padx=12, pady=12)

    tk.Label(sales_frame, text="Sales UI", font=("Arial", 14)).grid(row=0, column=0, columnspan=3, pady=10, sticky="w")

    tk.Label(sales_frame, text="Product Code").grid(row=1, column=0, sticky="w")
    code_entry = tk.Entry(sales_frame)
    code_entry.grid(row=1, column=1, sticky="we")

    tk.Label(sales_frame, text="Quantity").grid(row=2, column=0, sticky="w")
    qty_entry = tk.Entry(sales_frame)
    qty_entry.grid(row=2, column=1, sticky="we")

    cart_list = tk.Listbox(sales_frame, width=60, height=8)
    cart_list.grid(row=4, column=0, columnspan=3, pady=10, sticky="we")

    total_label = tk.Label(sales_frame, text="Total: $0.00")
    total_label.grid(row=5, column=0, columnspan=3, sticky="w")

    tk.Label(sales_frame, text="Cash Given").grid(row=6, column=0, sticky="w")
    cash_entry = tk.Entry(sales_frame)
    cash_entry.grid(row=6, column=1, sticky="we")
    change_label = tk.Label(sales_frame, text="Change: $0.00")
    change_label.grid(row=6, column=2, sticky="w")

    cart = []
    total = 0.0

    def recalc_total():
        nonlocal total
        total = sum(item["line_total"] for item in cart)
        total_label.config(text=f"Total: ${total:.2f}")

    def refresh_cart_list():
        cart_list.delete(0, tk.END)
        for item in cart:
            p = item["product"]
            disc_txt = f" (Disc {item['discount_applied']}%)" if item["discount_applied"] else ""
            exp_txt = ""
            if p["type"] == "fruits" and p["expiry_date"]:
                try:
                    exp_date = datetime.date.fromisoformat(p["expiry_date"])
                    if exp_date < datetime.date.today():
                        exp_txt = " (Expired)"
                except ValueError:
                    exp_txt = " (Invalid expiry)"
            cart_list.insert(tk.END, f"{p['code']} - {p['type']} x{item['qty']} = ${item['line_total']:.2f}{disc_txt}{exp_txt}")

    def add_to_cart():
        code = code_entry.get().strip()
        qty_str = qty_entry.get().strip()
        if not code or not qty_str:
            messagebox.showerror("Error", "Product code and quantity required")
            return
        try:
            qty = int(qty_str)
            if qty <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a positive integer")
            return

        inventory = load_inventory()
        product = next((p for p in inventory if p["code"] == code), None)
        if not product:
            messagebox.showerror("Error", "Product not found")
            return

        if product["type"] == "fruits" and product["expiry_date"]:
            try:
                expiry = datetime.date.fromisoformat(product["expiry_date"])
                if expiry < datetime.date.today():
                    cont = messagebox.askyesno("Expired", "Item expired. Continue?")
                    if not cont:
                        show_sales_ui()
                        return
           