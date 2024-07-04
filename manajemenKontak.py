import sqlite3
from tkinter import *
from tkinter import messagebox

# Fungsi untuk menghubungkan ke database dan membuat tabel jika belum ada
def connect_db():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS contacts
                 (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, email TEXT)''')
    conn.commit()
    conn.close()

# Fungsi untuk menambahkan kontak
def add_contact():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
              (name_var.get(), phone_var.get(), email_var.get()))
    conn.commit()
    conn.close()
    load_contacts()
    clear_fields()

# Fungsi untuk memuat kontak ke dalam listbox
def load_contacts():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute("SELECT * FROM contacts")
    rows = c.fetchall()
    conn.close()
    contact_list.delete(0, END)
    for row in rows:
        contact_list.insert(END, row)

# Fungsi untuk menghapus kontak
def delete_contact():
    selected_contact = contact_list.curselection()
    if selected_contact:
        contact_id = contact_list.get(selected_contact)[0]
        conn = sqlite3.connect('contacts.db')
        c = conn.cursor()
        c.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
        conn.commit()
        conn.close()
        load_contacts()
    else:
        messagebox.showwarning("Warning", "Select a contact to delete")

# Fungsi untuk mengedit kontak
def edit_contact():
    selected_contact = contact_list.curselection()
    if selected_contact:
        contact_id = contact_list.get(selected_contact)[0]
        conn = sqlite3.connect('contacts.db')
        c = conn.cursor()
        c.execute("UPDATE contacts SET name=?, phone=?, email=? WHERE id=?",
                  (name_var.get(), phone_var.get(), email_var.get(), contact_id))
        conn.commit()
        conn.close()
        load_contacts()
        clear_fields()
    else:
        messagebox.showwarning("Warning", "Select a contact to edit")

# Fungsi untuk mengisi field dengan data kontak yang dipilih
def fill_fields(event):
    selected_contact = contact_list.curselection()
    if selected_contact:
        contact = contact_list.get(selected_contact)
        name_var.set(contact[1])
        phone_var.set(contact[2])
        email_var.set(contact[3])

# Fungsi untuk menghapus isi field
def clear_fields():
    name_var.set("")
    phone_var.set("")
    email_var.set("")

# Setup GUI menggunakan tkinter
root = Tk()
root.title("Daftar Kontak")

# Variabel untuk input
name_var = StringVar()
phone_var = StringVar()
email_var = StringVar()

# Label dan Entry untuk nama
Label(root, text="Nama Kontak").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=name_var).grid(row=0, column=1, padx=10, pady=5)

# Label dan Entry untuk telepon
Label(root, text="Nomor HP").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=phone_var).grid(row=1, column=1, padx=10, pady=5)

# Label dan Entry untuk email
Label(root, text="Email").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=email_var).grid(row=2, column=1, padx=10, pady=5)

# Tombol untuk menambahkan, menghapus, dan mengedit kontak
Button(root, text="Tambah", command=add_contact).grid(row=3, column=0, padx=10, pady=5)
Button(root, text="Edit", command=edit_contact).grid(row=3, column=1, padx=10, pady=5)
Button(root, text="Hapus", command=delete_contact).grid(row=3, column=2, padx=10, pady=5)

# Listbox untuk menampilkan kontak
contact_list = Listbox(root, width=50)
contact_list.grid(row=4, column=0, columnspan=3, padx=10, pady=5)
contact_list.bind('<<ListboxSelect>>', fill_fields)

# Load kontak saat aplikasi dimulai
connect_db()
load_contacts()

root.mainloop()