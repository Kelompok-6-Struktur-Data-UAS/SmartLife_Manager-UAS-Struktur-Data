import tkinter as tk
from tkinter import messagebox
from modules.todo_queue import TodoQueue
from utils.file_manager import load_data, save_data
import os

DATA_PATH = os.path.join("data", "tasks.json")

class TodoWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("To-Do List")
        self.geometry("400x500")
        self.queue = TodoQueue()

        self.load_tasks()
        self.create_widgets()

    def create_widgets(self):
        self.task_entry = tk.Entry(self, width=30, font=("Arial", 12))
        self.task_entry.pack(pady=10)

        add_btn = tk.Button(self, text="Tambah Tugas", command=self.add_task)
        add_btn.pack()

        del_btn = tk.Button(self, text="Selesaikan Tugas (Dequeue)", command=self.remove_task)
        del_btn.pack(pady=5)

        self.listbox = tk.Listbox(self, width=40, height=15)
        self.listbox.pack(pady=10)
        self.update_listbox()

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.queue.enqueue(task)
            self.task_entry.delete(0, tk.END)
            self.update_listbox()
            self.save_tasks()

    def remove_task(self):
        task = self.queue.dequeue()
        if task:
            messagebox.showinfo("Tugas Diselesaikan", f"Tugas '{task}' telah diselesaikan.")
            self.update_listbox()
            self.save_tasks()
        else:
            messagebox.showwarning("Kosong", "Tidak ada tugas.")

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for task in self.queue.get_all_tasks():
            self.listbox.insert(tk.END, task)

    def load_tasks(self):
        tasks = load_data(DATA_PATH)
        for task in tasks:
            self.queue.enqueue(task)

    def save_tasks(self):
        tasks = self.queue.get_all_tasks()
        save_data(DATA_PATH, tasks)
