from tkinter import *
from tkinter import ttk, messagebox
import sqlite3


class Employee:
    def __init__(self, root_win):
        self.root = root_win
        self.root.geometry("1100x500+220+130")
        self.root.title("Gestion des Employés")
        self.root.config(bg="white")
        self.root.focus_force()
        # system variables
        self.searchOption_var = StringVar()
        self.searchText_var = StringVar()

        self.emp_id_var = StringVar()
        self.name_var = StringVar()
        self.contact_var = StringVar()
        self.gender_var = StringVar()
        self.dob_var = StringVar()
        self.doj_var = StringVar()
        self.email_var = StringVar()
        self.password_var = StringVar()
        self.usertype_var = StringVar()
        self.salary_var = StringVar()

        # title
        title = Label(self.root, text="Information de l'employé", font=("Lato", 14, "normal"), bg="#2EB086", fg="white")
        title.place(x=50, y=20, width=1000)
        # content
        # -----first row-----
        emp_id_label = Label(self.root, text="Emp ID", font=("Lato", 14, "normal"), bg="white")
        emp_id_label.place(x=50, y=70)

        gender_label = Label(self.root, text="Sexe", font=("Lato", 14, "normal"), bg="white")
        gender_label.place(x=350, y=70)

        contact_label = Label(self.root, text="Contact", font=("Lato", 14, "normal"), bg="white")
        contact_label.place(x=750, y=70)

        emp_id_txt = Entry(self.root, textvariable=self.emp_id_var, font=("Lato", 14, "normal"), bg="#EEE6CE", bd=1)
        emp_id_txt.place(x=150, y=70, width=180)
        gender_opt = ttk.Combobox(self.root, textvariable=self.gender_var, values=("Select", "Homme", "Femme"), state="readonly", justify=CENTER, font=("Lato", 14, "normal"))
        gender_opt.place(x=500, y=70, width=180)
        gender_opt.current(0)
        contact_txt = Entry(self.root, textvariable=self.contact_var, font=("Lato", 14, "normal"), bd=1, bg="#EEE6CE")
        contact_txt.place(x=850, y=70, width=180)

        # -----second row-----
        name_label = Label(self.root, text="Nom", font=("Lato", 14, "normal"), bg="white")
        name_label.place(x=50, y=110)
        dob_label = Label(self.root, text="Date Naiss", font=("Lato", 14, "normal"), bg="white")
        dob_label.place(x=350, y=110)
        doj_label = Label(self.root, text="Date Adh", font=("Lato", 14, "normal"), bg="white")
        doj_label.place(x=750, y=110)

        name_txt = Entry(self.root, textvariable=self.name_var, font=("Lato", 14, "normal"), bg="#EEE6CE", bd=1)
        name_txt.place(x=150, y=110, width=180)
        dob_txt = Entry(self.root, textvariable=self.dob_var, font=("Lato", 14, "normal"), bg="#EEE6CE", bd=1)
        dob_txt.place(x=500, y=110, width=180)
        doj_txt = Entry(self.root, textvariable=self.doj_var, font=("Lato", 14, "normal"), bd=1, bg="#EEE6CE")
        doj_txt.place(x=850, y=110, width=180)

        # -----third row-----
        email_label = Label(self.root, text="Email", font=("Lato", 14, "normal"), bg="white")
        email_label.place(x=50, y=150)
        password_label = Label(self.root, text="Password", font=("Lato", 14, "normal"), bg="white")
        password_label.place(x=350, y=150)
        user_type_label = Label(self.root, text="Type", font=("Lato", 14, "normal"), bg="white")
        user_type_label.place(x=750, y=150)

        email_txt = Entry(self.root, textvariable=self.email_var, font=("Lato", 14, "normal"), bg="#EEE6CE", bd=1)
        email_txt.place(x=150, y=150, width=180)
        password_txt = Entry(self.root, textvariable=self.password_var, font=("Lato", 14, "normal"), bg="#EEE6CE", bd=1)
        password_txt.place(x=500, y=150, width=180)
        user_type_opt = ttk.Combobox(self.root, textvariable=self.usertype_var, values=("Admin", "Employé"), state="readonly", justify=CENTER, font=("Lato", 14, "normal"))
        user_type_opt.place(x=850, y=150, width=180)
        user_type_opt.current(0)

        # -----fourth row-----
        address_label = Label(self.root, text="Adresse", font=("Lato", 14, "normal"), bg="white")
        address_label.place(x=50, y=190)
        salary_label = Label(self.root, text="Salaire", font=("Lato", 14, "normal"), bg="white")
        salary_label.place(x=500, y=190)

        self.address_txt = Text(self.root, font=("Lato", 14, "normal"), bg="#EEE6CE", bd=1)
        self.address_txt.place(x=150, y=190, width=300, height=60)
        salary_txt = Entry(self.root, textvariable=self.salary_var, font=("Lato", 14, "normal"), bg="#EEE6CE", bd=1)
        salary_txt.place(x=600, y=190, width=180)
        # buttons
        add_btn = Button(self.root, text="Ajouter", command=self.add_emp, font=("Lato", 11, "bold"), bg="#2EB086", fg="white", bd=3, cursor="hand2")
        add_btn.place(x=500, y=225, width=110, height=25)
        update_btn = Button(self.root, text="Modifier", command=self.update_emp, font=("Lato", 11, "bold"), bg="#0AA1DD", fg="white", bd=3, cursor="hand2")
        update_btn.place(x=620, y=225, width=110, height=25)
        delete_btn = Button(self.root, text="Supprimer", command=self.delete_emp, font=("Lato", 11, "bold"), bg="#B8405E", fg="white", bd=3, cursor="hand2")
        delete_btn.place(x=740, y=225, width=110, height=25)
        clear_btn = Button(self.root, text="Effacer", command=self.clear, font=("Lato", 11, "bold"), bg="#313552", fg="white", bd=3, cursor="hand2")
        clear_btn.place(x=860, y=225, width=110, height=25)

        # search employee
        search_frame = LabelFrame(self.root, text="Chercher un Employé", font=("Lato", 11, "normal"), bg="white", bd=2)
        search_frame.place(x=250, y=260, width=600, height=70)

        # search options
        options_box = ttk.Combobox(search_frame, textvariable=self.searchOption_var, values=("Selectionner", "Email", "Nom", "Contact"), state="readonly", justify=CENTER, font=("Lato", 11, "normal"))
        options_box.place(x=10, y=10, width=180)
        options_box.current(0)

        search_box = Entry(search_frame, textvariable=self.searchText_var, font=("Lato", 11, "normal"), bg="#EEE6CE")
        search_box.place(x=200, y=10, width=200, height=25)
        search_btn = Button(search_frame, text="Chercher", command=self.search_emp, font=("Lato", 11, "bold"), bg="#2EB086", fg="white", bd=3, cursor="hand2")
        search_btn.place(x=410, y=10, width=150, height=25)

        # employees list
        emp_list_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_list_frame.place(x=0, y=350, relwidth=1, height=150)

        scroll_y = Scrollbar(emp_list_frame, orient=VERTICAL)
        scroll_x = Scrollbar(emp_list_frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        list_columns = ("id", "nom", "email", "sexe", "contact", "date.naiss", "date.adh", "password", "type", "adresse", "salaire")
        self.emp_list_table = ttk.Treeview(emp_list_frame, columns=list_columns, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.emp_list_table.pack(fill=BOTH, expand=1)
        scroll_x.config(command=self.emp_list_table.xview)
        scroll_y.config(command=self.emp_list_table.yview)

        self.emp_list_table.heading("id", text="ID")
        self.emp_list_table.heading("nom", text="Nom")
        self.emp_list_table.heading("email", text="Email")
        self.emp_list_table.heading("sexe", text="Sexe")
        self.emp_list_table.heading("contact", text="Contact")
        self.emp_list_table.heading("date.naiss", text="Date.Naiss")
        self.emp_list_table.heading("date.adh", text="Date.Adh")
        self.emp_list_table.heading("password", text="Password")
        self.emp_list_table.heading("type", text="Type")
        self.emp_list_table.heading("adresse", text="Adresse")
        self.emp_list_table.heading("salaire", text="Salaire")
        self.emp_list_table["show"] = "headings"

        self.emp_list_table.column("id", width=90)
        self.emp_list_table.column("nom", width=100)
        self.emp_list_table.column("email", width=100)
        self.emp_list_table.column("sexe", width=100)
        self.emp_list_table.column("contact", width=100)
        self.emp_list_table.column("date.naiss", width=100)
        self.emp_list_table.column("date.adh", width=100)
        self.emp_list_table.column("password", width=100)
        self.emp_list_table.column("type", width=100)
        self.emp_list_table.column("adresse", width=100)
        self.emp_list_table.column("salaire", width=100)

        self.emp_list_table.bind("<ButtonRelease-1>", self.get_data)

        self.show_emp()

    # employee methods
    def add_emp(self):
        con = sqlite3.connect("system.db")
        cur = con.cursor()
        try:
            if self.emp_id_var.get() == "":
                messagebox.showerror("Erreur", "ID de l'employé doit être saisie", parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE id=?", (self.emp_id_var.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Erreur", "ID deja existant, saisir un autre", parent=self.root)
                else:
                    values_to_insert = (self.emp_id_var.get(),
                                        self.name_var.get(),
                                        self.email_var.get(),
                                        self.gender_var.get(),
                                        self.contact_var.get(),
                                        self.dob_var.get(),
                                        self.doj_var.get(),
                                        self.password_var.get(),
                                        self.usertype_var.get(),
                                        self.address_txt.get('1.0', END),
                                        self.salary_var.get()
                                        )
                    cur.execute("INSERT INTO employee (id, name, email, gender, contact, dob, doj, password, type, address, salary) VALUES (?,?,?,?,?,?,?,?,?,?,?)", values_to_insert)
                    con.commit()
                    messagebox.showinfo("Succès", "Employé est ajouté avec succès", parent=self.root)
                    self.show_emp()
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur: {str(ex)}", parent=self.root)

    def show_emp(self):
        con = sqlite3.connect("system.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM employee")
            rows = cur.fetchall()
            self.emp_list_table.delete(*self.emp_list_table.get_children())
            for row in rows:
                self.emp_list_table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur: {str(ex)}", parent=self.root)

    def get_data(self, ev):
        table_focus = self.emp_list_table.focus()
        table_content = (self.emp_list_table.item(table_focus))
        row = table_content["values"]
        print(row)

        self.emp_id_var.set(row[0])
        self.name_var.set(row[1])
        self.email_var.set(row[2])
        self.gender_var.set(row[3])
        self.contact_var.set(row[4])
        self.dob_var.set(row[5])
        self.doj_var.set(row[6])
        self.password_var.set(row[7])
        self.usertype_var.set(row[8])
        self.address_txt.delete('1.0', END)
        self.address_txt.insert(END, row[9])
        self.salary_var.set(row[10])

    def update_emp(self):
        con = sqlite3.connect("system.db")
        cur = con.cursor()
        try:
            if self.emp_id_var.get() == "":
                messagebox.showerror("Erreur", "ID de l'employé doit être saisi", parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE id=?", (self.emp_id_var.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Erreur", "ID de l'Employé Invalid", parent=self.root)
                else:
                    values_to_insert = (
                                        self.name_var.get(),
                                        self.email_var.get(),
                                        self.gender_var.get(),
                                        self.contact_var.get(),
                                        self.dob_var.get(),
                                        self.doj_var.get(),
                                        self.password_var.get(),
                                        self.usertype_var.get(),
                                        self.address_txt.get('1.0', END),
                                        self.salary_var.get(),
                                        self.emp_id_var.get(),
                                        )
                    cur.execute("UPDATE employee set name=?, email=?, gender=?, contact=?, dob=?, doj=?, password=?, type=?, address=?, salary=? where id=?", values_to_insert)
                    con.commit()
                    messagebox.showinfo("Succès", "Employé est modifié avec succès", parent=self.root)
                    self.show_emp()
                    con.close()
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur: {str(ex)}", parent=self.root)

    def delete_emp(self):
        con = sqlite3.connect('system.db')
        cur = con.cursor()
        try:
            if self.emp_id_var.get() == "":
                messagebox.showerror("Erreur", "ID de l'employé doit être saisi", parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE id=?", (self.emp_id_var.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Erreur", "ID de l'Employé Invalid", parent=self.root)
                else:
                    user_confirm = messagebox.askyesno("Confirmation", "Confirmer la suppression?", parent=self.root)
                    if user_confirm:
                        cur.execute("DELETE FROM employee WHERE id=?", (self.emp_id_var.get(),))
                        con.commit()
                        messagebox.showinfo("Succès", "Employé est supprimer avec succès", parent=self.root)
                        self.show_emp()
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur: {str(ex)}", parent=self.root)

    def clear(self):
        self.emp_id_var.set("")
        self.name_var.set("")
        self.email_var.set("")
        self.gender_var.set("Select")
        self.contact_var.set("")
        self.dob_var.set("")
        self.doj_var.set("")
        self.password_var.set("")
        self.usertype_var.set("Admin")
        self.address_txt.delete('1.0', END)
        self.salary_var.set("")
        self.searchText_var.set("")
        self.searchOption_var.set("Selectionner")
        self.show_emp()

    def search_emp(self):
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
                cur.execute("SELECT * FROM employee WHERE " + self.searchOption_var.get() + " LIKE '%" + self.searchText_var.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0 :
                    self.emp_list_table.delete(*self.emp_list_table.get_children())
                    for row in rows:
                        self.emp_list_table.insert('', END, values=row)
                else:
                    messagebox.showerror("Erreur", "Aucun employé trouvé!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur: {str(ex)}", parent=self.root)



if __name__ == "__main__":
    root = Tk()
    system = Employee(root)
    root.mainloop()
