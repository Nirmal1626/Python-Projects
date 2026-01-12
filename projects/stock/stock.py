import tkinter as tk
from tkinter import messagebox, ttk
import random

class StockApp:
    def _init_(self):
        self.balance = 10000.0
        self.market = {
            "AAPL": 150.0,
            "GOOG": 2800.0,
            "TSLA": 700.0,
            "AMZN": 3300.0
        }
        self.portfolio = {}

    def get_balance(self):
        return self.balance

    def get_market(self):
        return self.market

    def get_portfolio(self):
        return self.portfolio

    def buy_stock(self, stock, qty):
        stock = stock.upper()

        if stock not in self.market:
            return False, "Stock not found in market"

        cost = self.market[stock] * qty
        if cost > self.balance:
            return False, "Insufficient balance"

        self.balance -= cost
        self.portfolio[stock] = self.portfolio.get(stock, 0) + qty
        return True, f"Bought {qty} shares of {stock}"

    def sell_stock(self, stock, qty):
        stock = stock.upper()

        if stock not in self.portfolio or self.portfolio[stock] < qty:
            return False, "Not enough shares to sell"

        revenue = self.market[stock] * qty
        self.balance += revenue
        self.portfolio[stock] -= qty

        if self.portfolio[stock] == 0:
            del self.portfolio[stock]

        return True, f"Sold {qty} shares of {stock}"

    def update_market(self):
        for stock in self.market:
            change = random.uniform(-5, 5)
            self.market[stock] += change
            self.market[stock] = max(1, self.market[stock])


# ---------------- GUI (TKINTER) ----------------
class StockTradingUI:
    def _init_(self, root):
        self.root = root
        self.root.title("Stock Trading Simulator")
        self.root.geometry("800x500")
        self.root.configure(bg="#1a1a1a")

        self.app = StockApp()   # ✅ FIX: backend object created

        self.setup_ui()
        self.refresh_ui()

    def setup_ui(self):
        tk.Label(
            self.root,
            text="Stock Trading Simulator",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#1a1a1a"
        ).pack(pady=10)

        self.balance_label = tk.Label(
            self.root,
            font=("Arial", 14),
            fg="yellow",
            bg="#1a1a1a"
        )
        self.balance_label.pack()

        frame = tk.Frame(self.root, bg="#1a1a1a")
        frame.pack(pady=10)

        # Market
        market_frame = tk.LabelFrame(
            frame,
            text="Market",
            fg="white",
            bg="#1a1a1a",
            font=("Arial", 12, "bold")
        )
        market_frame.grid(row=0, column=0, padx=10)

        self.market_tree = ttk.Treeview(
            market_frame,
            columns=("Stock", "Price"),
            show="headings",
            height=10
        )
        self.market_tree.heading("Stock", text="Stock")
        self.market_tree.heading("Price", text="Price ($)")
        self.market_tree.pack(padx=10, pady=5)

        # Portfolio
        portfolio_frame = tk.LabelFrame(
            frame,
            text="Portfolio",
            fg="white",
            bg="#1a1a1a",
            font=("Arial", 12, "bold")
        )
        portfolio_frame.grid(row=0, column=1, padx=10)

        self.portfolio_tree = ttk.Treeview(
            portfolio_frame,
            columns=("Stock", "Qty"),
            show="headings",
            height=10
        )
        self.portfolio_tree.heading("Stock", text="Stock")
        self.portfolio_tree.heading("Qty", text="Quantity")
        self.portfolio_tree.pack(padx=10, pady=5)

        # Actions
        action_frame = tk.Frame(self.root, bg="#1a1a1a")
        action_frame.pack(pady=10)

        tk.Label(action_frame, text="Stock:", fg="white", bg="#1a1a1a").grid(row=0, column=0)
        self.stock_entry = tk.Entry(action_frame)
        self.stock_entry.grid(row=0, column=1)

        tk.Label(action_frame, text="Qty:", fg="white", bg="#1a1a1a").grid(row=0, column=2)
        self.qty_entry = tk.Entry(action_frame)
        self.qty_entry.grid(row=0, column=3)

        tk.Button(action_frame, text="Buy", command=self.buy_stock, bg="green", fg="white", width=10).grid(row=0, column=4, padx=5)
        tk.Button(action_frame, text="Sell", command=self.sell_stock, bg="red", fg="white", width=10).grid(row=0, column=5, padx=5)
        tk.Button(action_frame, text="Update Market", command=self.update_market, bg="blue", fg="white", width=15).grid(row=0, column=6, padx=5)

    def refresh_ui(self):
        self.balance_label.config(text=f"Balance: ${self.app.get_balance():,.2f}")

        for row in self.market_tree.get_children():
            self.market_tree.delete(row)
        for stock, price in self.app.get_market().items():
            self.market_tree.insert("", "end", values=(stock, f"{price:.2f}"))

        for row in self.portfolio_tree.get_children():
            self.portfolio_tree.delete(row)
        for stock, qty in self.app.get_portfolio().items():
            self.portfolio_tree.insert("", "end", values=(stock, qty))

    def buy_stock(self):
        stock = self.stock_entry.get()
        qty = self.qty_entry.get()

        if not qty.isdigit():
            messagebox.showerror("Error", "Invalid quantity")
            return

        _, msg = self.app.buy_stock(stock, int(qty))
        messagebox.showinfo("Transaction", msg)
        self.refresh_ui()

    def sell_stock(self):
        stock = self.stock_entry.get()
        qty = self.qty_entry.get()

        if not qty.isdigit():
            messagebox.showerror("Error", "Invalid quantity")
            return

        _, msg = self.app.sell_stock(stock, int(qty))
        messagebox.showinfo("Transaction", msg)
        self.refresh_ui()

    def update_market(self):
        self.app.update_market()
        messagebox.showinfo("Market", "Prices updated!")
        self.refresh_ui()


# ---------------- MAIN ----------------
if __name__ == "_main_":
    root = tk.Tk()
    StockTradingUI(root)
    root.mainloop()