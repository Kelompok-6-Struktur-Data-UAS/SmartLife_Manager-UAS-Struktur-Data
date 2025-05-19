import tkinter as tk
from tkinter import messagebox

from interface.todo_ui import TodoWindow


class SmartLifeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SmartLife Manager")
        self.geometry("500x500")
        self.configure(bg="#f0f0f0")

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self, text="SmartLife Manager", font=("Helvetica", 20, "bold"), bg="#f0f0f0")
        title.pack(pady=30)

        # Tombol Menu Fitur
        features = [
            ("📝 To-Do List", self.open_todo),
            ("📓 Notes", self.open_notes),
            ("📅 Schedule", self.open_schedule),
            ("📊 Stats", self.open_stats),
            ("👥 Contacts", self.open_contacts)
        ]

        for (text, command) in features:
            button = tk.Button(self, text=text, width=30, height=2, font=("Arial", 12), command=command)
            button.pack(pady=5)

    # Fungsi sementara, nanti akan mengarah ke GUI masing-masing fitur
    def open_todo(self):
        TodoWindow(self)

    def open_notes(self):
        messagebox.showinfo("Notes", "Fitur Notes akan dibuka.")

    def open_schedule(self):
        messagebox.showinfo("Schedule", "Fitur Jadwal akan dibuka.")

    def open_stats(self):
        messagebox.showinfo("Stats", "Fitur Statistik akan dibuka.")

    def open_contacts(self):
        messagebox.showinfo("Contacts", "Fitur Kontak akan dibuka.")