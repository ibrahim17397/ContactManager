import tkinter as tk
from tkinter import *
from tkinter import ttk
from cm_utils import *
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename



class Gui(tk.Frame):
    selected_item_id = None
    db = None
    fields = []
    order_filter = "first_name"


    #Get DB object, and draw gui components
    def __init__(self,root,db):
        self.db = db
        self.root= root
        self.root.title("Contacts Manager")
        self.root.resizable(0,0)
        frame = self.draw_form()
        self.draw_buttons(frame)
        self.draw_treeview()
        self.update_treeview()
        self.draw_menu_bar()


    #draw TextBoxes and labels of the form
    def draw_form(self):
        frame = LabelFrame(self.root,text="Add new Contact")
        frame.grid(row=0,column=0,columnspan=2,pady=25)
        Label (frame,text="First Name:").grid(row=1,column=1)
        self.firstname = Entry(frame,width=28)
        self.firstname.grid(row=1,column=2,columnspan=2)
        self.fields.append(self.firstname)

        Label(frame, text="Last Name:").grid(row=2, column=1)
        self.lastname = Entry(frame,width=28)
        self.lastname.grid(row=2, column=2,columnspan=2)
        self.fields.append(self.lastname)

        Label(frame, text="Phone:").grid(row=3, column=1)
        self.phone = Entry(frame,width=28)
        self.phone.grid(row=3, column=2,columnspan=2)
        self.fields.append(self.phone)

        Label(frame, text="Address:").grid(row=4, column=1)
        self.address = Entry(frame,width=28)
        self.address.grid(row=4, column=2,columnspan=2)
        self.fields.append(self.address)

        self.message=Label(text="",fg="red",pady=5)
        self.message.grid(row=3,column=0,columnspan=2)
        return frame


    #draw all button of the program
    def draw_buttons(self, frame):
        ttk.Button(frame,text="Add Contact",command=self.add_entry).grid(row=6,column=3)
        self.updateBtn = ttk.Button(frame,text="Update Contact",command=self.update_entry,state=DISABLED)
        self.updateBtn.grid(row=6,column=2)
        ttk.Button(text="Delete Contact",command=self.delete_entry).grid(row=5,column=0)
        ttk.Button(text="Edit Contact",command=self.fill_data).grid(row=5,column=1)


    #draw menu bar
    def draw_menu_bar(self):
        menu = Menu(self.root)
        self.root.config(menu=menu)
        file = Menu(menu, tearoff=False)
        file.add_command(label="Export..", command=self.export_as_sheet)

        menu.add_cascade(label="File", menu=file)

        about = Menu(menu, tearoff=False)
        about.add_command(label="credits", command=self.show_credits)
        menu.add_cascade(label="About", menu=about)



    def draw_treeview(self):
        self.tree=ttk.Treeview(height=10,columns=2)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree["columns"]=("first","second","third")
        self.tree.grid(row=4,column=0,columnspan=2)
        self.tree.heading('#0',text='First Name',anchor=W,command=lambda : self.order_entries_by("first_name"))
        self.tree.heading("first", text='Last Name', anchor=W,command=lambda : self.order_entries_by("last_name"))
        self.tree.heading("second", text='Phone', anchor=W,command=lambda : self.order_entries_by("phone_number"))
        self.tree.heading("third", text='Address', anchor=W,command=lambda : self.order_entries_by("address"))



    def order_entries_by(self,col_name):
        self.order_filter = col_name
        self.update_treeview()



    def add_entry(self):
        if self.validate_input() is True:
            self.db.insert_contact((self.firstname.get(), self.lastname.get(), self.phone.get(), self.address.get()))
            self.update_treeview()
            self.clear_data()
            self.message.configure(text="Contact was successfully added.",fg="green")
        else:
            self.message.configure(text="Please complete all fields.", fg="red")



    def update_treeview(self):
        self.tree.delete(*self.tree.get_children())
        db_rows = self.db.get_all_contacts(self.order_filter)
        for row in db_rows:
            self.tree.insert("","end", text=row[1], values=(row[2],row[3],row[4]),tag=row[0])



    def validate_input(self):
        for field in self.fields:
            if not field.get():
                return False
        return True



    def fill_data(self):
        result = list(self.db.get_contact(self.selected_item_id))[0]
        self.clear_data()
        for i in range(4):
            self.fields[i].insert(0, result[i+1])
        self.updateBtn.configure(state=NORMAL)



    def clear_data(self):
        for i in range(4):
            self.fields[i].delete(0, END)



    def on_tree_select(self, event):
        row_id = self.tree.item(self.tree.selection()[0],"tag")
        self.selected_item_id = int(row_id[0])



    def delete_entry(self):
        if self.selected_item_id is None:
            self.message.configure(text="Please select contact to delete.",fg="red")
        else:
            result = self.db.delete_contact(self.selected_item_id)
            self.update_treeview()
            self.message.configure(text="Contact was successfully deleted.",fg="green")



    def update_entry(self):
        if self.selected_item_id is None:
            self.message.configure(text="Please select contact to update.",fg="red")
        else:
            result = self.db.update_contact((self.firstname.get(), self.lastname.get(), self.phone.get(), self.address.get(), self.selected_item_id))
            self.update_treeview()
            self.clear_data()
            self.updateBtn.configure(state=DISABLED)
            self.message.configure(text="Contact was successfully updated.",fg="green")


    def export_as_sheet(self):
        filename = asksaveasfilename(parent=self.root,defaultextension=".xlsx")
        raw_contacts = self.db.get_all_contacts(self.order_filter)
        contacts = [list(contact)[1:] for contact in raw_contacts]
        writeXlsx(contacts,filename)
        self.message.configure(text="Exported all contacts successfully to\n{}.".format(filename),fg="green")


    def show_credits(self):
        credits = """
        Dynamic Programming Project 2019

        This Project was made with <3 by :

          - Ahmed Eid Ali
          - Ahmed Mohamed Elshrbiny
          - Ibrahim Ahmed Mubarak
          - Ibrahim Taha Ahmed
          - Hossam Mahmoud ElSayed
          - Mohamed Ali Farouk
        """
        messagebox.showinfo("Credits","ContactManager", detail=credits,parent=self.root)
