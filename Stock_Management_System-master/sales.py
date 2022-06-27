from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import os

class Sales:
    def __init__(self, root_win):
        self.root = root_win
        self.root.geometry("1100x500+220+130")
        self.root.title("Gestion des Ventes")
        self.root.config(bg="white")
        self.root.focus_force()
        # system variables

        self.invoice_var = StringVar()
        self.bills_list = []

        # title
        title = Label(self.root, text="Factures des Ventes", font=("Lato", 14, "normal"), bg="#2EB086", fg="white")
        title.place(x=50, y=20, width=1000)

        invoice_label = Label(self.root, text="Facture No.", font=("Lato", 14, "normal"), bg="white")
        invoice_label.place(x=50, y=80)
        invoice_txt = Entry(self.root, textvariable=self.invoice_var, font=("Lato", 14, "normal"), bg="#EEE6CE")
        invoice_txt.place(x=170, y=80, height=28)

        search_btn = Button(self.root, text="Chercher", command=self.search, font=("Lato", 14, "normal"), bg="#2EB086", fg="white", bd=0, cursor="hand2")
        search_btn.place(x=400, y=80, width=120, height=28)
        clear_btn = Button(self.root, text="Effacer", command=self.clear, font=("Lato", 14, "normal"), bg="#313552", fg="white", bd=0, cursor="hand2")
        clear_btn.place(x=530, y=80, width=120, height=28)

        # sales list
        sales_frame = Frame(self.root, bd=2)
        sales_frame.place(x=50, y=130, width=200,height=330)

        scroll_y = Scrollbar(sales_frame, orient=VERTICAL)
        scroll_x = Scrollbar(sales_frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        self.sales_list = Listbox(sales_frame, font=("Lato", 14, "normal"), bg="white")
        self.sales_list.pack(fill=BOTH,expand=1)
        scroll_x.config(command=self.sales_list.xview)
        scroll_y.config(command=self.sales_list.yview)
        self.sales_list.bind("<ButtonRelease-1>", self.get_data)

        # bills show areatitle = Label(self.root, text="Factures des Ventes", font=("Lato", 14, "normal"), bg="#2EB086", fg="white")
        title.place(x=50, y=20, width=1000)
        bill_frame = Frame(self.root, bd=2)
        bill_frame.place(x=280, y=130, width=410, height=330)
        title_bill = Label(bill_frame, text="Affichage Facture", font=("Lato", 14, "normal"), bg="#2EB086", fg="white")
        title_bill.pack(side=TOP, fill=X)
        scroll_bill_y = Scrollbar(bill_frame, orient=VERTICAL)
        scroll_bill_y.pack(side=RIGHT, fill=Y)
        self.bill_area = Text(bill_frame, font=("Lato", 12, "normal"), bg="#EEE6CE")
        self.bill_area.pack(fill=BOTH, expand=1)
        scroll_bill_y.config(command=self.bill_area.yview)

        # image
        self.bill_img = Image.open("images/sales_img.png")
        self.bill_img = self.bill_img.resize((400, 250))
        self.bill_img = ImageTk.PhotoImage(self.bill_img)

        img_label = Label(self.root, image=self.bill_img, bd=0)
        img_label.place(x=700, y=110)

        self.show()


        # sales methods

    def show(self):
        del self.bills_list[:]
        self.sales_list.delete(0, END)
        for i in os.listdir("bills"):
            if i.split(".")[-1] == "txt":
                self.sales_list.insert(END, i)
                self.bills_list.append(i.split(".")[0])

    def get_data(self, ev):
        row_index = self.sales_list.curselection()
        file_name = self.sales_list.get(row_index,)
        print(file_name)
        self.bill_area.delete('1.0', END)
        with open(f'bills/{file_name}', 'r') as file:
            for i in file:
                self.bill_area.insert(END, i)

    def search(self):
        if self.invoice_var.get() == "":
            messagebox.showerror("Erreur", "Facture No. obligatoire!", parent=self.root)
        else:
            if self.invoice_var.get() in self.bills_list:
                with open(f'bills/{self.invoice_var.get()}.txt', 'r') as file:
                    self.bill_area.delete("1.0", END)
                    for i in file:
                        self.bill_area.insert(END, i)
            else:
                messagebox.showerror("Erreur", "Facture non existante!", parent=self.root)

    def clear(self):
        self.show()
        self.bill_area.delete("1.0", END)
        self.invoice_var.set("")




if __name__ == "__main__":
    root = Tk()
    system = Sales(root)
    root.mainloop()
