from tkinter import *
from tkinter import ttk, messagebox
from employee import Employee
from supplier import Supplier
from category import Category
from product import Product
from sales import Sales
import sqlite3
import os
import threading


class StockManager:
    def __init__(self, root_win):
        self.root = root_win
        self.root.geometry("1350x700+0+0")
        self.root.title("Système de Gestion de Stock")
        self.root.config(bg="white")

        # screen Title
        title = Label(self.root, text="Tableau de Bord", font=("Lato", 26, "bold"), bg="white", fg="#343A40", anchor="w", padx=20) # may add anchor here to center left
        title.place(x=200, y=0, relwidth=1, height=70)

        # logout button
        logout_btn = Button(self.root, text="déconnexion", command=self.logout, font=("Lato", 11, "bold"), bd=0, bg="#F66B0E", fg="white")
        logout_btn.place(x=1180, y=10, height=40, width=120)

        # Menu
        menu_frame = Frame(self.root, bd=0, bg="#23282c", relief=RIDGE)
        menu_frame.place(x=0, y=0, width=200, height=400, relheight=1)

        menu_label = Label(menu_frame, text="Menu", font=("Lato", 15, "bold"), fg="#313552", bg="#23ba9b")
        menu_label.pack(side=TOP, fill=X)

        employee_btn = Button(menu_frame, text="Employés", command=self.employee, font=("Lato", 14, "normal"), bg="#23282c", fg="#a7acb2", bd=0, cursor="hand2")
        employee_btn.pack(side=TOP, fill=X)
        supplier_btn = Button(menu_frame, text="Fournisseurs", command=self.supplier, bg="#23282c", font=("Lato", 14, "normal"), fg="#a7acb2", bd=0, cursor="hand2")
        supplier_btn.pack(side=TOP, fill=X)
        product_btn = Button(menu_frame, text="Produits", command=self.product, font=("Lato", 14, "normal"), bg="#23282c", fg="#a7acb2", bd=0, cursor="hand2")
        product_btn.pack(side=TOP, fill=X)
        category_btn = Button(menu_frame, text="Catégories", command=self.category, font=("Lato", 14, "normal"), bg="#23282c", fg="#a7acb2", bd=0, cursor="hand2")
        category_btn.pack(side=TOP, fill=X)
        sales_btn = Button(menu_frame, text="Ventes", command=self.sales, font=("Lato", 14, "normal"), bg="#23282c", fg="#a7acb2", bd=0, cursor="hand2")
        sales_btn.pack(side=TOP, fill=X)
        quit_btn = Button(menu_frame, text="Quitter", font=("Lato", 14, "normal"), bg="#23282c", fg="#a7acb2", bd=0, cursor="hand2")
        quit_btn.pack(side=TOP, fill=X)

        # dashboard content
        self.employee_label = Label(self.root, text="Total des Employés\n0", font=("Lato", 15, "bold"), fg="white", bg="#f27b53", bd=5)
        self.employee_label.place(x=300, y=80, width=300, height=100)
        self.supplier_label = Label(self.root, text="Total des Fournisseurs\n0", font=("Lato", 15, "bold"), fg="white", bg="#dc587d", bd=5)
        self.supplier_label.place(x=650, y=80, width=300, height=100)
        self.product_label = Label(self.root, text="Total des Produits\n0", font=("Lato", 15, "bold"), fg="white", bg="#847cc5", bd=5)
        self.product_label.place(x=1000, y=80, width=300, height=100)
        self.category_label = Label(self.root, text="Total des Catégories\n0", font=("Lato", 15, "bold"), fg="white", bg="#fbb168", bd=5)
        self.category_label.place(x=300, y=200, width=300, height=100)
        self.sales_label = Label(self.root, text="Total des Ventes\n0", font=("Lato", 15, "bold"), fg="white", bg="#23ba9b", bd=5)
        self.sales_label.place(x=650, y=200, width=300, height=100)

        # sales list
        sales_list_frame = Frame(self.root, bd=3, relief=RIDGE)
        sales_list_frame.place(x=220, y=350, width=420, height=250)

        scroll_y = Scrollbar(sales_list_frame, orient=VERTICAL)
        scroll_x = Scrollbar(sales_list_frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        sales_list_columns = ("facture_no", "nom_client", "contact_client", "date")
        self.sales_list_table = ttk.Treeview(sales_list_frame, columns=sales_list_columns, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.sales_list_table.pack(fill=BOTH, expand=1)
        scroll_x.config(command=self.sales_list_table.xview)
        scroll_y.config(command=self.sales_list_table.yview)

        self.sales_list_table.heading("facture_no", text="Facture No.")
        self.sales_list_table.heading("nom_client", text="Nom Client")
        self.sales_list_table.heading("contact_client", text="Contact Client")
        self.sales_list_table.heading("date", text="Date")
        self.sales_list_table["show"] = "headings"

        self.sales_list_table.column("facture_no", width=100)
        self.sales_list_table.column("nom_client", width=100)
        self.sales_list_table.column("contact_client", width=100)
        self.sales_list_table.column("date", width=100)

        # line_sale list
        line_sale_list_columns = Frame(self.root, bd=3, relief=RIDGE)
        line_sale_list_columns.place(x=660, y=350, width=650, height=250)

        scroll_y = Scrollbar(line_sale_list_columns, orient=VERTICAL)
        scroll_x = Scrollbar(line_sale_list_columns, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        sales_list_columns = ("facture_no", "nom_prod", "prix", "qte")
        self.line_sale_list_table = ttk.Treeview(line_sale_list_columns, columns=sales_list_columns, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.line_sale_list_table.pack(fill=BOTH, expand=1)
        scroll_x.config(command=self.line_sale_list_table.xview)
        scroll_y.config(command=self.line_sale_list_table.yview)

        self.line_sale_list_table.heading("facture_no", text="Facture No.")
        self.line_sale_list_table.heading("nom_prod", text="Nom Produit")
        self.line_sale_list_table.heading("prix", text="Prix")
        self.line_sale_list_table.heading("qte", text="QTE")
        self.line_sale_list_table["show"] = "headings"

        self.line_sale_list_table.column("facture_no", width=100)
        self.line_sale_list_table.column("nom_prod", width=100)
        self.line_sale_list_table.column("prix", width=100)
        self.line_sale_list_table.column("qte", width=100)


        # footer
        footer = Label(self.root, text="will write footer here later", font=("Lato", 15, "normal"), bg="#2EB086", fg="#313552") # may add anchor here to center left
        footer.place(x=0, y=670, relwidth=1, height=30)

        self.update_content()
        self.show_sales()
        self.show_line_sale()
        # ========================================================

    def employee(self):
        self.new_window = Toplevel(self.root)
        self.emp_manager = Employee(self.new_window)

    def supplier(self):
        self.new_window = Toplevel(self.root)
        self.supp_manager = Supplier(self.new_window)

    def category(self):
        self.new_window = Toplevel(self.root)
        self.category_manager = Category(self.new_window)

    def product(self):
        self.new_window = Toplevel(self.root)
        self.product_manager = Product(self.new_window)

    def sales(self):
        self.new_window = Toplevel(self.root)
        self.sales_manager = Sales(self.new_window)

    def update_content(self):
        con = sqlite3.connect("system.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM employee")
            p = cur.fetchone()[0]
            self.employee_label.config(text=f"Total des Employés\n{p}")

            cur.execute("SELECT COUNT(*) FROM supplier")
            supp = cur.fetchone()[0]
            self.supplier_label.config(text=f"Total des Fournisseurs\n{supp}")

            cur.execute("SELECT COUNT(*) FROM product")
            prd = cur.fetchone()[0]
            self.product_label.config(text=f"Total des Produits\n{prd}")

            cur.execute("SELECT COUNT(*) FROM category")
            cat = cur.fetchone()[0]
            self.category_label.config(text=f"Total des Catégories\n{cat}")

            self.sales_label.config(text=f"Total des Ventes\n{str(len(os.listdir('bills')))}")

            threading.Timer(2.0, self.update_content).start()
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur: {str(ex)}", parent=self.root)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")

    def show_sales(self):
        con = sqlite3.connect("system.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM sales")
            rows = cur.fetchall()
            self.sales_list_table.delete(*self.sales_list_table.get_children())
            for row in rows:
                self.sales_list_table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur: {str(ex)}", parent=self.root)

    def show_line_sale(self):
        con = sqlite3.connect("system.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT ls.invoice, p.name, ls.price, ls.qty FROM line_sale ls JOIN product p ON ls.product_id=p.id")
            rows = cur.fetchall()
            self.line_sale_list_table.delete(*self.line_sale_list_table.get_children())
            for row in rows:
                self.line_sale_list_table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur: {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    system = StockManager(root)
    root.mainloop()
