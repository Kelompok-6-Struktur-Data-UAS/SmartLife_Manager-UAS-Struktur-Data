from interface.gui import SmartLifeApp

def main():
    app = SmartLifeApp()
    app.mainloop()

if __name__ == "__main__":
    main()
from interface.todo_ui import TodoWindow

def open_todo(self):
    TodoWindow(self)
