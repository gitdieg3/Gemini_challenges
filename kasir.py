import tkinter as tk
from tkinter import ttk, messagebox
import json, csv
from datetime import datetime

PRODUCT_FILE = "products.json"

def load_products():
    try:
        with open(PRODUCT_FILE, "r") as f:
            return json.load(f)
    except:
        return []

class KasirApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kasir Profesional - Pemesanan Barang")
        self.root.geometry("950x600")
        self.root.configure(bg="#e9edf5")

        self.products = load_products()
        self.cart = []

        # === HEADER ===
        header = tk.Frame(root, bg="#2c3e50", height=60)
        header.pack(side=tk.TOP, fill=tk.X)
        tk.Label(header, text="🛒 Kasir Profesional", fg="white", bg="#2c3e50",
                 font=("Segoe UI", 16, "bold")).pack(pady=10)

        # === FORM DATA PEMBELI ===
        buyer_frame = tk.Frame(root, bg="#ecf0f1")
        buyer_frame.pack(pady=10, fill="x")
        tk.Label(buyer_frame, text="Nama Pembeli:", bg="#ecf0f1", font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
        self.buyer_name = tk.StringVar()
        tk.Entry(buyer_frame, textvariable=self.buyer_name, width=30).pack(side="left", padx=5)

        self.date_now = datetime.now().strftime("%d %B %Y %H:%M:%S")
        tk.Label(buyer_frame, text=f"Tanggal: {self.date_now}", bg="#ecf0f1", font=("Segoe UI", 10, "italic")).pack(side="right", padx=10)

        # === PRODUK PILIHAN ===
        top_area = tk.Frame(root, bg="#ecf0f1")
        top_area.pack(pady=10)
        tk.Label(top_area, text="Produk:", bg="#ecf0f1").grid(row=0, column=0, padx=5)
        self.product_var = tk.StringVar()
        self.cmb_product = ttk.Combobox(top_area, textvariable=self.product_var, state="readonly", width=40)
        self.cmb_product["values"] = [f"{p['name']} - Rp{p['price']}" for p in self.products]
        self.cmb_product.grid(row=0, column=1, padx=5)

        tk.Label(top_area, text="Qty:", bg="#ecf0f1").grid(row=0, column=2, padx=5)
        self.qty_var = tk.IntVar(value=1)
        tk.Entry(top_area, textvariable=self.qty_var, width=5).grid(row=0, column=3, padx=5)

        tk.Button(top_area, text="➕ Tambah", bg="#27ae60", fg="white", command=self.add_to_cart).grid(row=0, column=4, padx=5)

        # === KERANJANG ===
        columns = ("Produk", "Harga", "Qty", "Subtotal")
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # === TOTAL + ACTIONS ===
        action_frame = tk.Frame(root, bg="#ecf0f1")
        action_frame.pack(pady=10, fill="x")

        tk.Button(action_frame, text="🗑 Hapus Item", bg="#c0392b", fg="white", command=self.remove_item).pack(side="left", padx=10)
        tk.Button(action_frame, text="💾 Checkout", bg="#2980b9", fg="white", command=self.checkout).pack(side="left", padx=10)

        self.lbl_total = tk.Label(action_frame, text="Total: Rp0", font=("Segoe UI", 12, "bold"), bg="#ecf0f1", fg="#2c3e50")
        self.lbl_total.pack(side="right", padx=20)

    def add_to_cart(self):
        selection = self.cmb_product.get()
        if not selection:
            messagebox.showwarning("Pilih Produk", "Silakan pilih produk dulu")
            return
        qty = self.qty_var.get()
        if qty <= 0:
            messagebox.showwarning("Jumlah Salah", "Jumlah harus lebih dari 0")
            return

        index = self.cmb_product.current()
        product = self.products[index]
        subtotal = product["price"] * qty
        self.cart.append({"name": product["name"], "price": product["price"], "qty": qty, "subtotal": subtotal})
        self.refresh_cart()

    def remove_item(self):
        selected = self.tree.selection()
        if not selected:
            return
        idx = self.tree.index(selected[0])
        self.cart.pop(idx)
        self.refresh_cart()

    def refresh_cart(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        total = 0
        for item in self.cart:
            self.tree.insert("", tk.END, values=(item["name"], f"Rp{item['price']}", item["qty"], f"Rp{item['subtotal']}"))
            total += item["subtotal"]
        self.lbl_total.config(text=f"Total: Rp{total:,}")

    def checkout(self):
        if not self.cart:
            messagebox.showwarning("Kosong", "Keranjang masih kosong")
            return
        if not self.buyer_name.get():
            messagebox.showwarning("Nama Kosong", "Masukkan nama pembeli")
            return

        filename = f"transaksi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Nama Pembeli", self.buyer_name.get()])
            writer.writerow(["Tanggal", self.date_now])
            writer.writerow([])
            writer.writerow(["Produk", "Harga", "Qty", "Subtotal"])
            for item in self.cart:
                writer.writerow([item["name"], item["price"], item["qty"], item["subtotal"]])
        messagebox.showinfo("Sukses", f"Transaksi berhasil!\nData tersimpan di {filename}")
        self.cart.clear()
        self.refresh_cart()
