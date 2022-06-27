from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk


class Category:
    def __init__(self, root_win):
        self.root = root_win
        self.root.geometry("1100x500+220+130")
        self.root.title("Gestion des Catégories")
        self.root.config(bg="white")
        self.root.focus_force()

        # system Variables
        self.categ_id_var = StringVar()
        self.categ_name_var = StringVar()
        # title
        title = Label(self.root, text="Gestion des Catégories", font=("Lato", 14, "normal"), bg="#2EB086", fg="white")
        title.place(x=50, y=20, width=1000)

        #content
        name_label = Label(self.root, text="Nom de Catégories", font=("Lato", 25, "normal"), bg="white")
        name_label.place(x=50, y=100)
        name_text = Entry(self.root, textvariable=self.categ_name_var, font=("Lato", 25, "normal"), bg="#EEE6CE", bd=1)
        name_text.place(x=50, y=160, width=300)

        add_btn = Button(self.root, text="Ajouter", command=self.add_categ, font=("Lato", 11, "bold"), bg="#2EB086", fg="white", bd=3, cursor="hand2")
        add_btn.place(x=370, y=160, width=110, height=40)
        delete_btn = Button(self.root, text="Supprimer", command=self.delete_categ, font=("Lato", 11, "bold"), bg="#B8405E", fg="white", bd=3, cursor="hand2")
        delete_btn.place(x=490, y=160, width=110, height=40)

        # category list
        categ_list_frame = Frame(self.root, bd=3, relief=RIDGE)
        categ_list_frame.place(x=700, y=100, width=380, height=100)

        scroll_y = Scrollbar(categ_list_frame, orient=VERTICAL)
        scroll_x = Scrollbar(categ_list_frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        list_columns = ("id", "nom")
        self.categ_list_tabel = ttk.Treeview(categ_list_frame, columns=list_columns, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.categ_list_tabel.pack(fill=BOTH, expand=1)
        scroll_x.config(command=self.categ_list_tabel.xview)
        scroll_y.config(command=self.categ_list_tabel.yview)

        self.categ_list_tabel.heading("id", text="ID")
        self.categ_list_tabel.heading("nom", text="Nom")

        self.categ_list_tabel["show"] = "headings"

        self.categ_list_tabel.column("id", width=90)
        self.categ_list_tabel.column("nom", width=100)

        self.categ_list_tabel.bind("<ButtonRelease-1>", self.get_data)

        self.show_categ()


        # image
        self.image = Image.open("images/stock_image.png")
        self.image = self.image.resize((900, 250))
        self.image = ImageTk.PhotoImage(self.image)
        self.image_label = Label(self.root, image=self.image)
        self.image_label.place(x=100, y=230)

        # category methods

    def add_categ(self):
        con = sqlite3.connect("system.db")
        cur = con.cursor()
        try:
            if self.categ_name_var.get() == "":
                messagebox.showerror("Erreur", "Nom de catégorie doit être saisie", parent=self.root)
            else:
                cur.execute("SELECT * FROM category WHERE name=?", (self.categ_name_var.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Erreur", "Catégorie deja existante, saisir un autre", parent=self.root)
                else:
                    values_to_insert = (
                                        self.categ_name_var.get(),
                                        )
                    cur.execute("INSERT INTO category (name) VALUES (?)", values_to_insert)
                    con.commit()
                    messagebox.showinfo("Succès", "Catégorie est ajouté avec succès", parent=self.root)
                    self.show_categ()
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur: {str(ex)}", parent=self.root)

    def show_categ(self):
        con = sqlite3.connect("system.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM category")
            rows = cur.fetchall()
            self.categ_list_tabel.delete(*self.categ_list_tabel.get_children())
            for row in rows:
                self.categ_list_tabel.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur: {str(ex)}", parent=self.root)

    def get_data(self, ev):
        table_focus = self.categ_list_tabel.focus()
        table_content = (self.categ_list_tabel.item(table_focus))
        row = table_content["values"]
        print(row)

        self.categ_id_var.set(row[0])
        self.categ_name_var.set(row[1])

    def delete_categ(self):
        con = sqlite3.connect('system.db')
        cur = con.cursor()
        try:
            if self.categ_id_var.get() == "":
                messagebox.showerror("Erreur", "catégorie doit être selectionnée", parent=self.root)
            else:
                cur.execute("SELECT * FROM category WHERE id=?", (self.categ_id_var.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Erreur", "ID de Catégorie Invalid", parent=self.root)
                else:
                    user_confirm = messagebox.askyesno("Confirmation", "Confirmer la suppression?", parent=self.root)
                    if user_confirm:
                        cur.execute("DELETE FROM category WHERE id=?", (self.categ_id_var.get(),))
                        con.commit()
                        messagebox.showinfo("Succès", "Catégorie est supprimée avec succès", parent=self.root)
                        self.show_categ()
                        self.categ_id_var.set("")
                        self.categ_name_var.set("")

        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur: {str(ex)}", parent=self.root)



if __name__ == "__main__":
    root = Tk()
    system = Category(root)
    root.mainloop()
