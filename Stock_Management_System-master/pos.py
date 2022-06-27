from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import time
import os

class POS:
    def __init__(self, root_win):
        self.root = root_win
        self.root.geometry("1350x700+0+0")
        self.root.title("Système de Gestion de Stock")
        self.root.config(bg="white")

        # screen Title
        title = Label(self.root, text="Point de Vente", font=("Lato", 26, "bold"), bg="white", fg="#343A40", anchor="w", padx=20) # may add anchor here to center left
        title.place(x=10, y=0, relwidth=1, height=70)

        # logout button
        logout_btn = Button(self.root, text="déconnexion", command=self.logout, font=("Lato", 11, "bold"), bd=0, bg="#F66B0E", fg="white")
        logout_btn.place(x=1180, y=10, height=40, width=120)

        # product Frame ----------------------------------

        # produt search variable
        self.search_var = StringVar()

        product_frame = Frame(self.root, bd=1, relief=RIDGE, bg="white")
        product_frame.place(x=10, y=110, width=410, height=550)

        product_title = Label(product_frame, text="Section des Produits", font=("Lato", 14, "normal"),  bg="#2EB086", fg="white")
        product_title.pack(side=TOP, fill=X)

        product_search_frame = Frame(product_frame, bd=1, relief=RIDGE, bg="white")
        product_search_frame.place(x=2, y=36, width=399, height=90)

        search_label = Label(product_search_frame, text="Recherche de Produit", font=("Lato", 14, "normal"), bg="white", fg="#2EB086")
        search_label.place(x=2, y=5)
        pd_name_label = Label(product_search_frame, text="Nom de produit", font=("Lato", 13, "normal"), bg="white")
        pd_name_label.place(x=2, y=40)
        pd_name_txt = Entry(product_search_frame, textvariable=self.search_var, font=("Lato", 13, "normal"), bg="#EEE6CE")
        pd_name_txt.place(x=125, y=40, width=150, height=22)
        search_btn = Button(product_search_frame, text="Chercher", command=self.search_product, font=("Lato", 13, "normal"), bg="#2EB086", fg="white")
        search_btn.place(x=280, y=40, width=110, height=22)
        show_all_btn = Button(product_search_frame, text="Afficher tout", command=self.show_product, font=("Lato", 13, "normal"), bg="#313552",fg="white")
        show_all_btn.place(x=280, y=65, width=110, height=22)

        # product list
        product_list_frame = Frame(product_frame, bd=3, relief=RIDGE)
        product_list_frame.place(x=2, y=130, width=399, height=385)

        scroll_y = Scrollbar(product_list_frame, orient=VERTICAL)
        scroll_x = Scrollbar(product_list_frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        list_columns = ("id", "nom", "prix", "qte", "status")
        self.product_list_table = ttk.Treeview(product_list_frame, columns=list_columns, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.product_list_table.pack(fill=BOTH, expand=1)
        scroll_x.config(command=self.product_list_table.xview)
        scroll_y.config(command=self.product_list_table.yview)

        self.product_list_table.heading("id", text="ID")
        self.product_list_table.heading("nom", text="Nom")
        self.product_list_table.heading("prix", text="Prix")
        self.product_list_table.heading("qte", text="QTE")
        self.product_list_table.heading("status", text="Status")

        self.product_list_table["show"] = "headings"

        self.product_list_table.column("id", width=40)
        self.product_list_table.column("nom", width=100)
        self.product_list_table.column("prix", width=80)
        self.product_list_table.column("qte", width=100)
        self.product_list_table.column("status", width=50)
        self.product_list_table.bind("<ButtonRelease-1>", self.get_data)

        note_label = Label(product_frame, text="Note: Entrez 0 pour enlever le produit du panier", font=("Lato", 12, "normal"), fg="#B22727", bg="white")
        note_label.pack(side=BOTTOM, fill=X)

        # customer frame

        # variables customer
        self.cust_name_var = StringVar()
        self.cust_contact_var = StringVar()
        customer_frame = Frame(self.root, bd=3, relief=RIDGE, background="white")
        customer_frame.place(x=420, y=110, width=530, height=70)

        cust_title = Label(customer_frame, text="Information du client", font=("Lato", 14, "normal"), bg="#2EB086", fg="white")
        cust_title.pack(side=TOP, fill=X)

        cust_name_label = Label(customer_frame, text="Nom", font=("Lato", 14, "normal"), bg="white")
        cust_name_label.place(x=5, y=35)
        cust_name_txt = Entry(customer_frame, textvariable=self.cust_name_var, font=("Lato", 14, "normal"), bg="#EEE6CE")
        cust_name_txt.place(x=80, y=35, width=180)

        cust_contact_label = Label(customer_frame, text="Contact No.", font=("Lato", 14, "normal"), bg="white")
        cust_contact_label.place(x=270, y=35)
        cust_contact_txt = Entry(customer_frame, textvariable=self.cust_contact_var, font=("Lato", 14, "normal"), bg="#EEE6CE")
        cust_contact_txt.place(x=380, y=35, width=140)

        # cart frame ---------------------------------------
        self.cart_list = []

        cal_cart_frame = Frame(self.root, bd=2, relief=RIDGE)
        cal_cart_frame.place(x=420, y=190, width=530, height=360)

        cart_frame = Frame(cal_cart_frame, bd=2, relief=RIDGE)
        cart_frame.place(x=2, y=3, relwidth=1, height=340)
        self.cart_title = Label(cart_frame, text="Panier   | \tTotal des Produits:  0 ", font=("Lato", 14, "normal"), bg="#2EB086", fg="white")
        self.cart_title.pack(side=TOP, fill=X)

        scroll_y = Scrollbar(cart_frame, orient=VERTICAL)
        scroll_x = Scrollbar(cart_frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        list_columns_cart = ("id", "nom", "prix", "qte", "stock")
        self.cart_list_table = ttk.Treeview(cart_frame, columns=list_columns_cart, yscrollcommand=scroll_y.set,
                                            xscrollcommand=scroll_x.set)
        self.cart_list_table.pack(fill=BOTH, expand=1)
        scroll_x.config(command=self.cart_list_table.xview)
        scroll_y.config(command=self.cart_list_table.yview)

        self.cart_list_table.heading("id", text="ID")
        self.cart_list_table.heading("nom", text="Nom")
        self.cart_list_table.heading("prix", text="Prix")
        self.cart_list_table.heading("qte", text="QTE")
        self.cart_list_table.heading("stock", text="Stock")
        self.cart_list_table["show"] = "headings"

        self.cart_list_table.column("id", width=90)
        self.cart_list_table.column("nom", width=100)
        self.cart_list_table.column("prix", width=100)
        self.cart_list_table.column("qte", width=100)
        self.cart_list_table.column("stock", width=100)
        self.cart_list_table.bind("<ButtonRelease-1>", self.get_cart_data)

        # cart widgets
        self.p_id_var = StringVar()
        self.p_name_var = StringVar()
        self.p_price_var = StringVar()
        self.p_qty_var = StringVar()
        self.p_stock_var = StringVar()
        cart_widgets_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        cart_widgets_frame.place(x=420, y=550, width=530, height=110)

        p_name_label = Label(cart_widgets_frame, text="Nom de produit", font=("Lato", 13, "normal"), bg="white")
        p_name_label.place(x=5, y=5)
        p_name_text = Entry(cart_widgets_frame, textvariable=self.p_name_var, font=("Lato", 13, "normal"), state="readonly", bg="#EEE6CE")
        p_name_text.place(x=5, y=35, width=190, height=22)

        p_price_label = Label(cart_widgets_frame, text="Prix par Qte", font=("Lato", 13, "normal"), bg="white")
        p_price_label.place(x=230, y=5)
        p_price_text = Entry(cart_widgets_frame, textvariable=self.p_price_var, font=("Lato", 13, "normal"), state="readonly", bg="#EEE6CE")
        p_price_text.place(x=230, y=35, width=150, height=22)

        p_qty_label = Label(cart_widgets_frame, text="Quantité", font=("Lato", 13, "normal"), bg="white")
        p_qty_label.place(x=400, y=5)
        p_qty_text = Entry(cart_widgets_frame, textvariable=self.p_qty_var, font=("Lato", 13, "normal"), bg="#EEE6CE")
        p_qty_text.place(x=400, y=35, width=120, height=22)

        self.p_stock_label = Label(cart_widgets_frame, text="En Stock", font=("Lato", 13, "normal"), bg="white")
        self.p_stock_label.place(x=5, y=70)

        add_cart_btn = Button(cart_widgets_frame, text="Ajouter au Panier", command=self.add_cart, font=("Lato", 12, "normal"), bg="#0AA1DD", fg="white")
        add_cart_btn.place(x=180, y=70, width=150, height=30)
        clear_cart_btn = Button(cart_widgets_frame, text="Effacer", command=self.clear_cart, font=("Lato", 12, "normal"), bg="#313552", fg="white")
        clear_cart_btn.place(x=340, y=70, width=150, height=30)

        # billing frame -----------------------------------------------------
        bill_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        bill_frame.place(x=953, y=110, width=390, height=410)

        bill_title = Label(bill_frame, text="Facture du Client", font=("Lato", 14, "normal"), bg="#2EB086", fg="white")
        bill_title.pack(side=TOP, fill=X)
        bill_scroll_y = Scrollbar(bill_frame, orient=VERTICAL)
        bill_scroll_y.pack(side=RIGHT, fill=Y)
        self.bill_area_text = Text(bill_frame, yscrollcommand=bill_scroll_y.set)
        self.bill_area_text.pack(fill=BOTH, expand=1)
        bill_scroll_y.config(command=self.bill_area_text.yview)

        # billing buttons ----------------------------------------------------------
        bill_menu_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        bill_menu_frame.place(x=953, y=520, width=390, height=140)

        self.amount_label = Label(bill_menu_frame, text="Montant\n0", font=("Lato", 14, "normal"), bg="#f27b53", fg="white")
        self.amount_label.place(x=5, y=5, width=120, height=70)

        self.discount_label = Label(bill_menu_frame, text="Réduction\n5%", font=("Lato", 14, "normal"), bg="#dc587d", fg="white")
        self.discount_label.place(x=130, y=5, width=120, height=70)

        self.net_label = Label(bill_menu_frame, text="Net à Payer\n0", font=("Lato", 14, "normal"), bg="#847cc5", fg="white")
        self.net_label.place(x=255, y=5, width=125, height=70)

        print_bnt = Button(bill_menu_frame, text="Imprimer", font=("Lato", 14, "normal"), bg="#2EB086", fg="white")
        print_bnt.place(x=5, y=80, width=120, height=50)

        generate_btn = Button(bill_menu_frame, text="Générer\nFacture", command=self.generate_bill, font=("Lato", 14, "normal"), bg="#0AA1DD", fg="white")
        generate_btn.place(x=130, y=80, width=120, height=50)

        clear_all_btn = Button(bill_menu_frame, text="Effacer\nTout", command=self.clear_all, font=("Lato", 14, "normal"),bg="#313552", fg="white")
        clear_all_btn.place(x=255, y=80, width=125, height=50)

        self.show_product()

    # methods ----------------------
    def show_product(self):
        con = sqlite3.connect("system.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT id, name, price, qty, status FROM product Where status='actif'")
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
            if self.search_var.get() == "":
                messagebox.showerror("Erreur", "Champ de recherche vide", parent=self.root)
            else:
                cur.execute("SELECT id, name, price, qty, status FROM product WHERE name LIKE '%" + self.search_var.get() + "%' and status='actif'")
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

        self.p_id_var.set(row[0])
        self.p_name_var.set(row[1])
        self.p_price_var.set(row[2])
        self.p_stock_var.set(row[3])
        self.p_qty_var.set("1")
        self.p_stock_label.config(text=f"En Stock: {row[3]}")

    def get_cart_data(self, ev):
        table_focus = self.cart_list_table.focus()
        table_content = (self.cart_list_table.item(table_focus))
        row = table_content["values"]

        self.p_id_var.set(row[0])
        self.p_name_var.set(row[1])
        self.p_price_var.set(row[2])
        self.p_qty_var.set(row[3])

    def add_cart(self):
        if self.p_id_var.get() == "":
            messagebox.showerror("Erreur", "Veuillez Selectionner Un Produit", parent=self.root)
        elif self.p_qty_var.get() == "":
            messagebox.showerror("Erreur", "Veuillez Saisir Quantité", parent=self.root)
        elif int(self.p_qty_var.get()) > int(self.p_stock_var.get()):
            messagebox.showerror("Erreur", "Stock insuffisant", parent=self.root)
        else:
            calculated_price = float(int(self.p_qty_var.get()) * float(self.p_price_var.get()))
            print(calculated_price)
            cart_data = [self.p_id_var.get(), self.p_name_var.get(), calculated_price, self.p_qty_var.get(), self.p_stock_var.get()]

            # to update cart
            product_exists = False
            index = 0
            for row in self.cart_list:
                if self.p_id_var.get() == row[0]:
                    product_exists = True
                    break
                index += 1

            if product_exists:
                op = messagebox.askyesno("Confirmation", "Produit existe deja. Voulez vous mettre a jour ?")
                if op:
                    if self.p_qty_var.get() == "0":
                        self.cart_list.pop(index)
                    else:
                        self.cart_list[index][2] = calculated_price
                        self.cart_list[index][3] = self.p_qty_var.get()
            else:
                self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_update()

    def show_cart(self):
        try:
            self.cart_list_table.delete(*self.cart_list_table.get_children())
            for row in self.cart_list:
                self.cart_list_table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur: {str(ex)}", parent=self.root)

    def bill_update(self):
        self.amount = 0
        self.net_pay = 0
        self.discount = 0
        for row in self.cart_list:
            self.amount = self.amount + float(row[2])
        self.discount = (self.amount * 5)/100
        self.net_pay = self.amount - self.discount

        self.amount_label.config(text=f"Montant\n{self.amount}DH")
        self.net_label.config(text=f"Net à Payer\n{self.net_pay}DH")
        self.cart_title.config(text=f"Panier   | \tTotal des Produits:  {len(self.cart_list)} ")


    def generate_bill(self):
        if self.cust_name_var.get() == "" or self.cust_contact_var.get() == "":
            messagebox.showerror("Erreur", f"Veuillez saisir les données du client", parent=self.root)
        elif len(self.cart_list) == 0:
            messagebox.showerror("Erreur", f"Veuillez ajouter des produits au panier", parent=self.root)
        else:
            # bill Top
            self.bill_top()
            # bill middle
            self.bill_middle()
            # bill bottom
            self.bill_bottom()

            with open(f"bills/{str(self.invoice_n)}.txt", "w") as f:
                f.write(self.bill_area_text.get("1.0", END))
            messagebox.showinfo("Succès", "Facture enregistrée", parent=self.root)


    def bill_top(self):
        self.invoice_n = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))
        print(self.invoice_n)
        bill_top_temp = f'''
\tRapimarket-Inventaire
\tTelephone No. 8899773344 , Marrakech
{str("="*45)}
Nom du Client: {self.cust_name_var.get()}
Tel client : {self.cust_contact_var.get()}
Facture No. {str(self.invoice_n)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*45)}
Nom Produit\t\t\tQTE\tPrix
{str("="*45)}
        '''
        self.bill_area_text.delete('1.0', END)
        self.bill_area_text.insert('1.0', bill_top_temp)

        con = sqlite3.connect("system.db")
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO sales VALUES (?,?,?,?)", (self.invoice_n, self.cust_name_var.get(), self.cust_contact_var.get(),str(time.strftime("%d/%m/%Y"))))
            con.commit()
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur: {str(ex)}", parent=self.root)

    def bill_middle(self):
        con = sqlite3.connect("system.db")
        cur = con.cursor()
        try:
            for row in self.cart_list:
                id = row[0]
                name = row[1]
                qty = row[3]
                price = row[2]
                print(row[4])
                self.bill_area_text.insert(END, "\n " + str(name) + "\t\t\t" + str(qty) + "\tDH " + str(price))
                product_stock = row[4]
                updated_qty = int(product_stock) - int(qty)
                if int(updated_qty) == 0:
                    status = "inactif"
                else:
                    status = "actif"
                cur.execute("UPDATE product set qty=?, status=? where id=?", (updated_qty, status, id))
                cur.execute("INSERT INTO line_sale VALUES (?,?,?,?)", (self.invoice_n, id, price, qty))
            con.commit()
            self.show_product()
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur: {str(ex)}", parent=self.root)

    def bill_bottom(self):
        bill_bottom_temp = f'''
{str("="*45)}
Montant Total\t\t\t\tDH {self.amount}
Réduction\t\t\t\tDH {self.discount}
Net à Payer\t\t\t\tDH {self.net_pay}
{str("="*45)}\n
        '''
        self.bill_area_text.insert(END, bill_bottom_temp)

    def clear_cart(self):
        self.p_id_var.set("")
        self.p_name_var.set("")
        self.p_price_var.set("")
        self.p_qty_var.set("")
        self.p_stock_label.config(text=f"En Stock")
        self.p_stock_var.set("")

    def clear_all(self):
        del self.cart_list[:]
        self.cust_name_var.set("")
        self.cust_contact_var.set("")
        self.bill_area_text.delete('1.0', END)
        self.cart_title.config(text=f"Panier   | \tTotal des Produits:  0")
        self.clear_cart()
        self.show_product()
        self.show_cart()

    def logout(self):
        self.root.destroy()
        os.system("python login.py")


if __name__ == "__main__":
    root = Tk()
    system = POS(root)
    root.mainloop()
