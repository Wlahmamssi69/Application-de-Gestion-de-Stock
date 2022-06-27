from tkinter import *
from tkinter import ttk, messagebox
import sqlite3


class Product:
    def __init__(self, root_win):
        self.root = root_win
        self.root.geometry("1100x500+220+130")
        self.root.title("Gestion des Produits")
        self.root.config(bg="white")
        self.root.focus_force()

        # system variables
        self.searchOption_var = StringVar()
        self.searchText_var = StringVar()

        self.prod_id_var = StringVar()
        self.categ_var = StringVar()
        self.supp_var = StringVar()
        self.categ_list = []
        self.supp_list = []
        self.get_categ_supp()

        self.name_var = StringVar()
        self.price_var = StringVar()
        self.qty_var = StringVar()
        self.status_var = StringVar()

        product_frame = Frame(self.root, bd=1, bg="white")
        product_frame.place(x=10, y=10, width=500, height=480)

        title = Label(product_frame, text="Information des Produits", font=("Lato", 14, "normal"), bg="#2EB086", fg="white")
        title.pack(side=TOP, fill=X)

        # labels
        categ_label = Label(product_frame, text="Catégorie", font=("Lato", 14, "normal"), bg="white")
        categ_label.place(x=30, y=60)
        supp_label = Label(product_frame, text="Fournisseur", font=("Lato", 14, "normal"), bg="white")
        supp_label.place(x=30, y=110)
        name_label = Label(product_frame, text="Nom", font=("Lato", 14, "normal"), bg="white")
        name_label.place(x=30, y=160)
        price_label = Label(product_frame, text="Prix", font=("Lato", 14, "normal"), bg="white")
        price_label.place(x=30, y=210)
        qty_label = Label(product_frame, text="Quantité", font=("Lato", 14, "normal"), bg="white")
        qty_label.place(x=30, y=260)
        status_label = Label(product_frame, text="Status", font=("Lato", 14, "normal"), bg="white")
        status_label.place(x=30, y=310)

        # inputs

        # category select
        categ_select = ttk.Combobox(self.root, textvariable=self.categ_var, values=self.categ_list, state="readonly", justify=CENTER, font=("Lato", 14, "normal"))
        categ_select.place(x=190, y=70, width=200)
        categ_select.current(0)
        # supplier select
        supp_select = ttk.Combobox(self.root, textvariable=self.supp_var, values=self.supp_list, state="readonly", justify=CENTER, font=("Lato", 14, "normal"))
        supp_select.place(x=190, y=120, width=200)
        supp_select.current(0)

        name_txt = Entry(product_frame, textvariable=self.name_var, font=("Lato", 14, "normal"), bg="#EEE6CE", bd=1)
        name_txt.place(x=180, y=160, width=200)
        price_txt = Entry(product_frame, textvariable=self.price_var, font=("Lato", 14, "normal"), bg="#EEE6CE", bd=1)
        price_txt.place(x=180, y=210, width=200)
        qty_txt = Entry(product_frame, textvariable=self.qty_var, font=("Lato", 14, "normal"), bg="#EEE6CE", bd=1)
        qty_txt.place(x=180, y=260, width=200)

        status_select = ttk.Combobox(self.root, textvariable=self.status_var, values=("actif", "inactif"), state="readonly", justify=CENTER, font=("Lato", 14, "normal"))
        status_select.place(x=190, y=320, width=200)
        status_select.current(0)

        # buttons
        add_btn = Button(product_frame, text="Ajouter", command=self.add_product, font=("Lato", 11, "bold"), bg="#2EB086", fg="white", bd=3, cursor="hand2")
        add_btn.place(x=10, y=400, width=110, height=25)
        update_btn = Button(product_frame, text="Modifier", command=self.update_product, font=("Lato", 11, "bold"), bg="#0AA1DD", fg="white", bd=3, cursor="hand2")
        update_btn.place(x=130, y=400, width=110, height=25)
        delete_btn = Button(product_frame, text="Supprimer", command=self.delete_product, font=("Lato", 11, "bold"), bg="#B8405E", fg="white", bd=3, cursor="hand2")
        delete_btn.place(x=250, y=400, width=110, height=25)
        clear_btn = Button(product_frame, text="Effacer", command=self.clear, font=("Lato", 11, "bold"), bg="#313552", fg="white", bd=3, cursor="hand2")
        clear_btn.place(x=370, y=400, width=110, height=25)

        # search employee
        search_frame = LabelFrame(self.root, text="Chercher un Produit", font=("Lato", 11, "normal"), bg="white", bd=2)
        search_frame.place(x=520, y=10, width=465, height=70)

        # search options
        options_box = ttk.Combobox(search_frame, textvariable=self.searchOption_var, values=("Selectionner", "Catégorie", "Fournisseur", "Nom"), state="readonly", justify=CENTER, font=("Lato", 11, "normal"))
        options_box.place(x=10, y=10, width=150)
        options_box.current(0)

        search_box = Entry(search_frame, textvariable=self.searchText_var, font=("Lato", 11, "normal"), bg="#EEE6CE")
        search_box.place(x=170, y=10, width=170, height=25)
        search_btn = Button(search_frame, text="Chercher", command=self.search_product, font=("Lato", 11, "bold"), bg="#2EB086", fg="white", bd=3, cursor="hand2")
        search_btn.place(x=350, y=10, width=100, height=25)

        # Products list
        product_list_frame = Frame(self.root, bd=3, relief=RIDGE)
        product_list_frame.place(x=520, y=90, width=560, height=390)

        scroll_y = Scrollbar(product_list_frame, orient=VERTICAL)
        scroll_x = Scrollbar(product_list_frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        list_columns = ("id", "Categorie", "Fournisseur", "Nom", "Prix", "Qte", "Status")
        self.product_list_table = ttk.Treeview(product_list_frame, columns=list_columns, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.product_list_table.pack(fill=BOTH, expand=1)
        scroll_x.config(command=self.product_list_table.xview)
        scroll_y.config(command=self.product_list_table.yview)

        self.product_list_table.heading("id", text="ID")
        self.product_list_table.heading("Categorie", text="Catégorie")
        self.product_list_table.heading("Fournisseur", text="Fournissuer")
        self.product_list_table.heading("Nom", text="Nom")
        self.product_list_table.heading("Prix", text="Prix")
        self.product_list_table.heading("Qte", text="Qté")
        self.product_list_table.heading("Status", text="Status")
        self.product_list_table["show"] = "headings"

        self.product_list_table.column("id", width=90)
        self.product_list_table.column("Categorie", width=100)
        self.product_list_table.column("Fournisseur", width=100)
        self.product_list_table.column("Nom", width=100)
        self.product_list_table.column("Prix", width=100)
        self.product_list_table.column("Qte", width=100)
        self.product_list_table.column("Status", width=100)

        self.product_list_table.bind("<ButtonRelease-1>", self.get_data)

        self.show_product()

        # product methods
    def get_categ_supp(self):
        self.categ_list.append("Vide")
        self.supp_list.append("Vide")
        con = sqlite3.connect("system.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT name FROM category")
            categs = cur.fetchall()

            if len(categs) > 0:
                del self.categ_list[:]
                self.categ_list.append("Select")
                for item in categs:
                    self.categ_list.append(item[0])

            cur.execute("SELECT name FROM supplier")
            suppls = cur.fetchall()

            if len(suppls) > 0:
                del self.supp_list[:]
                self.supp_list.append("Select")
                for item in suppls:
                    self.supp_list.append(item[0])
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur: {str(ex)}", parent=self.root)

    def add_product(self):
        con = sqlite3.connect("system.db")
        cur = con.cursor()
        try:
            if self.categ_var.get() == "Vide" or self.supp_var.get() == "Vide" :
                messagebox.showerror("Erreur", "Vous devez remplir d'abord les catégories et fournisseurs", parent=self.root)
            elif self.categ_var.get() == "Select" or self.supp_var.get() == "Select" or self.name_var.get() == "":
                messagebox.showerror("Erreur", "Les champs catégorie, fournisseur, et Nom sont obligatoires", parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE name=?", (self.name_var.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Erreur", "Produit deja existant", parent=self.root)
                else:
                    values_to_insert = (self.categ_var.get(),
                                        self.supp_var.get(),
                                        self.name_var.get(),
                                        self.price_var.get(),
                                        self.qty_var.get(),
                                        self.status_var.get(),
                                        )
                    cur.execute("INSERT INTO product (category, supplier, name, price, qty, status) VALUES (?,?,?,?,?,?)", values_to_insert)
                    con.commit()
                    messagebox.showinfo("Succès", "Produit ajouté avec succès", parent=self.root)
                    self.show_product()
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur: {str(ex)}", parent=self.root)

    def update_product(self):
        con = sqlite3.connect("system.db")
        cur = con.cursor()
        try:
            if self.prod_id_var.get() == "":
                messagebox.showerror("Erreur", "Vous devez selectionner un produit de la liste", parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE id=?", (self.prod_id_var.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Erreur", "ID de Produit Invalid", parent=self.root)
                else:
                    values_to_insert = (
                                        self.categ_var.get(),
                                        self.supp_var.get(),
                                        self.name_var.get(),
                                        self.price_var.get(),
                                        self.qty_var.get(),
                                        self.status_var.get(),
                                        self.prod_id_var.get()
                                        )
                    cur.execute("UPDATE product set category=?, supplier=?, name=?, price=?, qty=?, status=? WHERE id=?", values_to_insert)
                    con.commit()
                    messagebox.showinfo("Succès", "Produit modifié avec succès", parent=self.root)
                    self.show_product()
                    con.close()
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur: {str(ex)}", parent=self.root)

    def delete_product(self):
        con = sqlite3.connect('system.db')
        cur = con.cursor()
        try:
            if self.prod_id_var.get() == "":
                messagebox.showerror("Erreur", "Vous devez selectionner un produit de la liste", parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE id=?", (self.prod_id_var.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Erreur", "ID du Produit Invalid", parent=self.root)
                else:
                    user_confirm = messagebox.askyesno("Confirmation", "Confirmer la suppression?", parent=self.root)
                    if user_confirm:
                        cur.execute("DELETE FROM product WHERE id=?", (self.prod_id_var.get(),))
                        con.commit()
                        messagebox.showinfo("Succès", "Produit supprimer avec succès", parent=self.root)
                        self.show_product()
                        # self.clear()

        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur: {str(ex)}", parent=self.root)

    def show_product(self):
        con = sqlite3.connect("system.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM product")
            rows = cur.fetchall()
            self.product_list_table.delete(*self.product_list_table.get_children())
            for row in rows:
                self.product_list_table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur: {str(ex)}", parent=self.root)

    def search_product(self):
        con = sqlite3.connect('system.db')
        cur = con.cursor()
        try:
            if self.searchOption_var.get() == "Selectionner":
                messagebox.showerror("Erreur", "Selectionner l'option de recherche", parent=self.root)
            elif self.searchText_var.get() == "":
                messagebox.showerror("Erreur", "Champ de recherche vide", parent=self.root)
            else:
                if self.searchOption_var.get() == "Nom":
                    self.searchOption_var.set("name")
                elif self.searchOption_var.get() == "Catégorie":
                    self.searchOption_var.set("category")
                elif self.searchOption_var.get() == "Fournisseur":
                    self.searchOption_var.set("supplier")
                cur.execute("SELECT * FROM product WHERE " + self.searchOption_var.get() + " LIKE '%" + self.searchText_var.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0 :
                    self.product_list_table.delete(*self.product_list_table.get_children())
                    for row in rows:
                        self.product_list_table.insert('', END, values=row)
                else:
                    messagebox.showerror("Erreur", "Aucun Produit trouvé!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur: {str(ex)}", parent=self.root)


    def get_data(self, ev):
        table_focus = self.product_list_table.focus()
        table_content = (self.product_list_table.item(table_focus))
        row = table_content["values"]
        print(row)

        self.prod_id_var.set(row[0])
        self.categ_var.set(row[1])
        self.supp_var.set(row[2])
        self.name_var.set(row[3])
        self.price_var.set(row[4])
        self.qty_var.set(row[5])
        self.status_var.set(row[6])

    def clear(self):
        self.prod_id_var.set("")
        self.categ_var.set("Select")
        self.supp_var.set("Select")
        self.name_var.set("")
        self.price_var.set("")
        self.qty_var.set("")
        self.status_var.set("")
        self.show_product()


if __name__ == "__main__":
    root = Tk()
    system = Product(root)
    root.mainloop()
