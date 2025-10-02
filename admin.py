import tkinter as tk
from tkinter import ttk, messagebox
import json
import os, sys

PRODUCT_FILE = "products.json"

def load_products():
    try:
        with open(PRODUCT_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_products(products):
    with open(PRODUCT_FILE, "w") as f:
        json.dump(products, f, indent=4)

def admin_panel():
    def add_product():
        name = entry_name.get().strip()
        price = entry_price.get().strip()
        if not name or not price:
            messagebox.showwarning("Input Error", "Nama dan harga wajib diisi")
            return
        try:
            price = int(price)
        except:
            messagebox.showerror("Error", "Harga harus angka")
            return
        
        products = load_products()
        products.append({"name": name, "price": price})
        save_products(products)
        entry_name.delete(0, tk.END)
        entry_price.delete(0, tk.END)
        refresh_list()
        messagebox.showinfo("Sukses", f"Produk {name} ditambahkan")

    def delete_product():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Pilih Produk", "Silakan pilih produk yang ingin dihapus")
            return
        index = int(tree.item(selected[0], "text"))
        products = load_products()
        deleted = products.pop(index)
        save_products(products)
        refresh_list()
        messagebox.showinfo("Dihapus", f"Produk {deleted['name']} dihapus")

    def edit_product():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Pilih Produk", "Silakan pilih produk yang ingin diubah")
            return
        index = int(tree.item(selected[0], "text"))
        products = load_products()

        edit_win = tk.Toplevel(root)
        edit_win.title("Edit Produk")
        edit_win.geometry("300x200")

        tk.Label(edit_win, text="Nama Baru:").pack(pady=5)
        name_var = tk.Entry(edit_win)
        name_var.pack(pady=5)
        name_var.insert(0, products[index]['name'])

        tk.Label(edit_win, text="Harga Baru:").pack(pady=5)
        price_var = tk.Entry(edit_win)
        price_var.pack(pady=5)
        price_var.insert(0, products[index]['price'])

        def save_edit():
            try:
                new_price = int(price_var.get())
            except:
                messagebox.showerror("Error", "Harga harus angka")
                return
            products[index]['name'] = name_var.get().strip()
            products[index]['price'] = new_price
            save_products(products)
            refresh_list()
            edit_win.destroy()
            messagebox.showinfo("Sukses", "Produk berhasil diperbarui")

        ttk.Button(edit_win, text="Simpan", command=save_edit).pack(pady=10)

    def search_product(*args):
        keyword = search_var.get().lower()
        for row in tree.get_children():
            tree.delete(row)
        for i, p in enumerate(load_products()):
            if keyword in p['name'].lower():
                tree.insert("", "end", text=str(i), values=(p['name'], f"Rp{p['price']}"))
        update_total()

    def refresh_list():
        for row in tree.get_children():
            tree.delete(row)
        for i, p in enumerate(load_products()):
            tree.insert("", "end", text=str(i), values=(p['name'], f"Rp{p['price']}"))
        update_total()

    def update_total():
        total = len(load_products())
        lbl_total.config(text=f"Total Produk: {total}")

    def logout():
        root.destroy()
        # panggil kembali main.py (login)
        os.system(f"{sys.executable} main.py")

    # === Main Admin Panel ===
    root = tk.Tk()
    root.title("Admin Panel - Kelola Produk")
    root.geometry("600x500")
    root.configure(bg="#f8f9fa")

    # Header dengan tombol logout
    header = tk.Frame(root, bg="#2c3e50", height=50)
    header.pack(fill="x")
    tk.Label(header, text="📦 Admin Panel - Manajemen Produk", 
             font=("Segoe UI", 14, "bold"), bg="#2c3e50", fg="white").pack(side="left", padx=10, pady=10)
    ttk.Button(header, text="🚪 Logout", command=logout).pack(side="right", padx=10, pady=10)

    # Form tambah produk
    form_frame = tk.Frame(root, bg="#f8f9fa")
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Nama Barang:", font=("Segoe UI", 10), bg="#f8f9fa").grid(row=0, column=0, sticky="w", padx=5, pady=3)
    entry_name = ttk.Entry(form_frame, width=30)
    entry_name.grid(row=0, column=1, padx=5, pady=3)

    tk.Label(form_frame, text="Harga Barang:", font=("Segoe UI", 10), bg="#f8f9fa").grid(row=1, column=0, sticky="w", padx=5, pady=3)
    entry_price = ttk.Entry(form_frame, width=30)
    entry_price.grid(row=1, column=1, padx=5, pady=3)

    ttk.Button(form_frame, text="➕ Tambah Produk", command=add_product).grid(row=2, column=0, columnspan=2, pady=10)

    # Search bar
    search_frame = tk.Frame(root, bg="#f8f9fa")
    search_frame.pack(pady=5, fill="x")
    tk.Label(search_frame, text="🔍 Cari Produk:", font=("Segoe UI", 10), bg="#f8f9fa").pack(side="left", padx=5)
    search_var = tk.StringVar()
    search_var.trace("w", search_product)
    ttk.Entry(search_frame, textvariable=search_var, width=30).pack(side="left", padx=5)

    # Tabel produk
    table_frame = tk.Frame(root, bg="#f8f9fa")
    table_frame.pack(pady=10, fill="both", expand=True)

    columns = ("Nama", "Harga")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    tree.heading("Nama", text="Nama Produk")
    tree.heading("Harga", text="Harga")
    tree.column("Nama", width=250)
    tree.column("Harga", width=100)

    vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=vsb.set)
    tree.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")

    # Tombol aksi
    btn_frame = tk.Frame(root, bg="#f8f9fa")
    btn_frame.pack(pady=5)

    ttk.Button(btn_frame, text="✏ Edit Produk", command=edit_product).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="🗑 Hapus Produk", command=delete_product).pack(side="left", padx=5)

    # Total produk
    lbl_total = tk.Label(root, text="Total Produk: 0", font=("Segoe UI", 10, "bold"), bg="#f8f9fa", fg="#212529")
    lbl_total.pack(anchor="e", padx=10, pady=5)

    refresh_list()
    root.mainloop()

if __name__ == "__main__":
    admin_panel()
