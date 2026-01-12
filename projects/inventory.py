import tkinter as tk
from tkinter import ttk, messagebox


class InventoryApp:
    def __init__(self):
        self.inventory = {}

    def get_inventory(self):
        return self.inventory

    def add_item(self, item, price, qty):
        item = item.lower()
        if item in self.inventory:
            self.inventory[item]["quantity"] += qty
        else:
            self.inventory[item] = {"price": price, "quantity": qty}

    def update_item(self, item, price, qty):
        item = item.lower()
        if item in self.inventory:
            self.inventory[item] = {"price": price, "quantity": qty}
            return True
        return False

    def sell_item(self, item, qty):
        item = item.lower()
        if item not in self.inventory:
            return False, "Item not found in inventory."
        if self.inventory[item]["quantity"] < qty:
            return False, "Insufficient quantity."
        self.inventory[item]["quantity"] -= qty
        return True, f"Sold {qty} unit(s) of {item}."

    def delete_item(self, item):
        item = item.lower()
        if item in self.inventory:
            del self.inventory[item]
            return True
        return False


class InventoryUI:
    def __init__(self, root):
        self.app = InventoryApp()
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("900x600")
        self.root.config(bg="#101820")

        self.setup_ui()
        self.refresh_table()

    def setup_ui(self):
        # Header
        tk.Label(
            self.root,
            text="Inventory Management System",
            font=("Helvetica", 22, "bold"),
            bg="#101820",
            fg="#FEE715"
        ).pack(pady=15)

        # Input frame
        input_frame = tk.Frame(self.root, bg="#101820")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Item Name:", bg="#101820", fg="white", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
        self.item_entry = tk.Entry(input_frame, font=("Arial", 12), width=20)
        self.item_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(input_frame, text="Price (₹):", bg="#101820", fg="white", font=("Arial", 12)).grid(row=0, column=2, padx=10, pady=5)
        self.price_entry = tk.Entry(input_frame, font=("Arial", 12), width=10)
        self.price_entry.grid(row=0, column=3, padx=10, pady=5)

        tk.Label(input_frame, text="Quantity:", bg="#101820", fg="white", font=("Arial", 12)).grid(row=0, column=4, padx=10, pady=5)
        self.qty_entry = tk.Entry(input_frame, font=("Arial", 12), width=10)
        self.qty_entry.grid(row=0, column=5, padx=10, pady=5)

        # Button frame
        button_frame = tk.Frame(self.root, bg="#101820")
        button_frame.pack(pady=5)

        btn_style = {"font": ("Arial", 11, "bold"), "width": 12, "bd": 0, "pady": 5, "fg": "white"}

        tk.Button(button_frame, text="Add Item", bg="#28A745", command=self.add_item, **btn_style).grid(row=0, column=0, padx=8)
        tk.Button(button_frame, text="Update Item", bg="#007BFF", command=self.update_item, **btn_style).grid(row=0, column=1, padx=8)
        tk.Button(button_frame, text="Sell Item", bg="#FFC107", command=self.sell_item, **btn_style).grid(row=0, column=2, padx=8)
        tk.Button(button_frame, text="Delete Item", bg="#DC3545", command=self.delete_item, **btn_style).grid(row=0, column=3, padx=8)
        tk.Button(button_frame, text="Refresh", bg="#6C757D", command=self.refresh_table, **btn_style).grid(row=0, column=4, padx=8)

        # Inventory table
        table_frame = tk.Frame(self.root)
        table_frame.pack(pady=20)

        style = ttk.Style()
        style.configure("mystyle.Treeview", font=("Arial", 11), rowheight=30, background="#F2F2F2")
        style.configure("mystyle.Treeview.Heading", font=("Arial", 12, "bold"))

        columns = ("Item", "Price", "Quantity", "Total Value")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", style="mystyle.Treeview", height=12)

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center", width=150)

        self.table.pack(fill="both", expand=True)

    def refresh_table(self):
        for row in self.table.get_children():
            self.table.delete(row)

        for item, data in self.app.get_inventory().items():
            total_value = data["price"] * data["quantity"]
            self.table.insert("", "end", values=(item.capitalize(), f"₹{data['price']}", data["quantity"], f"₹{total_value}"))

    def add_item(self):
        item = self.item_entry.get().strip()
        price = self.price_entry.get().strip()
        qty = self.qty_entry.get().strip()

        if not item or not price.isdigit() or not qty.isdigit():
            messagebox.showerror("Error", "Enter valid item, price, and quantity.")
            return

        self.app.add_item(item, int(price), int(qty))
        messagebox.showinfo("Success", f"{item.capitalize()} added/updated successfully.")
        self.refresh_table()

    def update_item(self):
        item = self.item_entry.get().strip()
        price = self.price_entry.get().strip()
        qty = self.qty_entry.get().strip()

        if not item or not price.isdigit() or not qty.isdigit():
            messagebox.showerror("Error", "Enter valid item, price, and quantity.")
            return

        success = self.app.update_item(item, int(price), int(qty))
        if success:
            messagebox.showinfo("Success", f"{item.capitalize()} updated successfully.")
        else:
            messagebox.showerror("Error", "Item not found in inventory.")
        self.refresh_table()

    def sell_item(self):
        item = self.item_entry.get().strip()
        qty = self.qty_entry.get().strip()

        if not item or not qty.isdigit():
            messagebox.showerror("Error", "Enter valid item and quantity.")
            return

        success, msg = self.app.sell_item(item, int(qty))
        if success:
            messagebox.showinfo("Sale Complete", msg)
        else:
            messagebox.showerror("Error", msg)
        self.refresh_table()

    def delete_item(self):
        item = self.item_entry.get().strip()
        if not item:
            messagebox.showerror("Error", "Enter item name to delete.")
            return

        success = self.app.delete_item(item)
        if success:
            messagebox.showinfo("Deleted", f"{item.capitalize()} removed from inventory.")
        else:
            messagebox.showerror("Error", "Item not found.")
        self.refresh_table()


if __name__ == "__main__":
    root = tk.Tk()
    ui = InventoryUI(root)
    root.mainloop()
