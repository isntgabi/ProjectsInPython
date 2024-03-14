import tkinter as tk  # interfata
from tkinter import messagebox
from cryptography.fernet import Fernet
import json
import os


class PasswordManager:
    def __init__(self, file_path):
        # initializare cale catre fisierul de stocare al datelor(respectiv parolelor)
        self.file_path = file_path
        # initializam o cheie de crypting/decrypting
        self.key = None
        self.passwords = {}  # dictionar de parole, initializat gol

    def generate_key(self):
        # generez o cheie de criptare random
        self.key = Fernet.generate_key()

    def load_key(self):
        if not os.path.exists("key.key"):  # verificam daca avem fisierul key existent
            self.generate_key()  # daca nu, generam o cheie
            with open("key.key", "wb") as key_file:  # wb - scriere binara, deschidem fisierul cheii
                key_file.write(self.key)  # scriem cheia in fisier, sub format binar
        else:
            with open("key.key", "rb") as key_file:  # deschidem cu rb fisierul, citire binara
                self.key = key_file.read()

    def load_passwords(self):
        if os.path.exists(self.file_path): #verificam daca acest fisier cu parole exista
            with open(self.file_path, "rb") as file:
                encrypted_data = file.read()
            fernet = Fernet(self.key) #initializam un obiect fernet care are cheia
            decrypted_data = fernet.decrypt(encrypted_data) #decriptare
            self.passwords = json.loads(decrypted_data)

    def save_passwords(self):
        fernet = Fernet(self.key)
        encrypted_data=fernet.encrypt(json.dumps(self.passwords).encode()) #criptarea datelor
        with open(self.file_path, "wb") as file:
            file.write(encrypted_data)

    def add_password(self,service,username,password): #creez un dictionar unde adaug parola
        self.passwords[service] = {"username": username, "password": password}
        self.save_passwords()

    def get_password(self, service):
        return self.passwords.get(service, None) #intorc parola pentru serviciu

    def list_services(self):
        return list(self.passwords.keys())

if __name__ == "__main__":
    file_path = "passwords.dat" #fisierul de stocare al parolelor - binar
    manager = PasswordManager(file_path) #obiect de tipul clasei
    manager.load_key()
    manager.load_passwords()

    #INTERFATA
    root = tk.Tk()
    root.title("Managing my passwords: ")

    service_entry = tk.Entry(root)
    username_entry = tk.Entry(root)
    password_entry = tk.Entry(root, show="*")

    #functia de adaugare parola
    def add_password():
        service = service_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        manager.add_password(service,username,password)
        messagebox.showinfo("SUCCESS!", "Password added successfully!")

    def get_password():
        service = service_entry.get()
        data = manager.get_password(service)
        if data:
            messagebox.showinfo("Password details:", f"Username: {data['username']}\nPassword: {data['password']}")
        else:
            messagebox.showerror("Error", "Platform not found!")
# etichetele de introducere
service_label = tk.Label(root, text="Platform:")
service_label.grid(row=0, column=0, padx=10, pady=5)
service_entry = tk.Entry(root)
service_entry.grid(row=0, column=1, padx=10, pady=5)

username_label = tk.Label(root, text="Username:")
username_label.grid(row=1, column=0, padx=10, pady=5)
username_entry = tk.Entry(root)
username_entry.grid(row=1, column=1, padx=10, pady=5)

password_label = tk.Label(root, text="Password:")
password_label.grid(row=2, column=0, padx=10, pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=2, column=1, padx=10, pady=5)

# Butonul de adaugare a parolei
add_button = tk.Button(root, text="Add Password", command=add_password)
add_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="WE")

# Buton pentru intoarcere parola
get_button = tk.Button(root, text="Get Password", command=get_password)
get_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="WE")

# START bucla pentru utilizator
root.mainloop()